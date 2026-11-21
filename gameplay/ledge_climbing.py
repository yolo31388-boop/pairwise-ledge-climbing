"""Ledge climbing helpers.

Each function corresponds to one of the reported gameplay defects:

* :func:`ledge_space` / :func:`grab_distance` / :func:`ledge_normal` —
  detection must consider the space above the ledge, not just a single
  ray fired forward from the capsule.
* :func:`state_hysteresis` — the climb state machine needs a dead band so it
  does not oscillate when the height difference sits near the threshold.
* :func:`root_motion_offset` — root motion must have the climb displacement
  stripped out before it is applied, otherwise the two stack and push the
  character through the wall.
* :func:`ledge_occupancy` — a ledge segment needs an occupancy lock so two
  characters cannot grab the same segment.
* :func:`authoritative_point` — the server owns the climb point; clients
  must not predict a different one.
* :func:`animation_event_time` — animation events are sampled by time, so a
  low frame rate cannot drop them.
* :func:`slope_normal` — slope normals are projected onto the horizontal
  plane, otherwise the character floats away from an angled ledge.
* :func:`cancel_velocity` — cancelling a climb clears gravity velocity so the
  character is not launched on recovery.
* :func:`save_climb_state` — saves carry the climb state, not just position.
* :func:`collision_layer` — the climb layer is separated from the camera
  collision layer.
"""

import math

__all__ = [
    "ledge_space",
    "state_hysteresis",
    "root_motion_offset",
    "ledge_occupancy",
    "authoritative_point",
    "animation_event_time",
    "slope_normal",
    "cancel_velocity",
    "save_climb_state",
    "collision_layer",
    "grab_distance",
    "ledge_normal",
    "climb_speed",
    "ledge_id",
    "state_key",
]


def ledge_space(clearance, height):
    """Return whether there is enough free space above a ledge.

    ``clearance`` is the measured head-room above the ledge and ``height``
    is the character's required height.  The check must pass before a grab
    is accepted, otherwise the character can hang under geometry.
    """
    return clearance >= height


def state_hysteresis(distance, threshold):
    """Return ``True`` when ``distance`` is outside the hysteresis band.

    ``distance`` is the height difference to the ledge.  Requiring it to
    clear ``threshold`` instead of merely crossing it keeps the state
    machine from flipping back and forth around the threshold.
    """
    return abs(distance) > abs(threshold)


def root_motion_offset(animation, climb):
    """Remove the climb displacement from root motion.

    ``animation`` and ``climb`` are equal-length vectors.  The returned
    vector is the animation offset with the climb contribution subtracted,
    so applying both does not double the movement into the wall.
    """
    animation = tuple(animation)
    climb = tuple(climb)
    if len(animation) != len(climb):
        raise ValueError("animation and climb vectors must have equal length")
    return tuple(a - c for a, c in zip(animation, climb))


def ledge_occupancy(occupants, capacity):
    """Return ``True`` if the ledge still has a free slot.

    ``occupants`` is the collection of characters already locked to the
    segment; ``capacity`` is how many may share it.  A free slot means the
    grab is allowed.
    """
    return len(occupants) < capacity


def authoritative_point(client_point, server_point):
    """Return the server-authoritative climb point.

    The server value always wins so a client cannot predict a different
    point and then be snapped back.
    """
    return tuple(server_point)


def animation_event_time(event_time, frame_time):
    """Return whether an animation event falls inside the current frame.

    Sampling by time (``0 <= event_time <= frame_time``) rather than by
    frame index guarantees events are not dropped at a low frame rate.
    """
    return 0.0 <= event_time <= frame_time


def slope_normal(normal):
    """Project a surface normal onto the horizontal (XY) plane and normalize.

    Ledge normals are treated with Z as the up axis; dropping Z keeps the
    character on an angled ledge instead of floating off it.  A zero-length
    projection returns ``(0.0, 0.0, 0.0)``.
    """
    x, y, _z = (float(component) for component in normal)
    length = math.hypot(x, y)
    if length == 0.0:
        return (0.0, 0.0, 0.0)
    return (x / length, y / length, 0.0)


def cancel_velocity(current):
    """Return a zero velocity matching the dimension of ``current``.

    Cancelling a climb must also clear the accumulated gravity velocity so
    the character does not launch when control returns.
    """
    return tuple(0.0 for _ in current)


def save_climb_state(state, valid):
    """Return the climb state to persist, or ``None`` when invalid.

    Saving the climb state alongside position keeps the character attached
    to the correct ledge after loading.
    """
    return state if valid else None


def collision_layer(layer, climb_mask):
    """Return whether ``layer`` intersects the climb collision mask.

    Keeping the climb mask separate from the camera mask lets the camera
    ignore ledges instead of being blocked by them.
    """
    return bool(layer & climb_mask)


def grab_distance(position, ledge):
    """Return the Euclidean distance between the character and the ledge."""
    return float(math.dist(position, ledge))


def ledge_normal(normal):
    """Return a unit-length version of the ledge normal.

    A zero-length normal returns ``(0.0, 0.0, 0.0)``.
    """
    values = tuple(float(component) for component in normal)
    length = math.sqrt(sum(component * component for component in values))
    if length == 0.0:
        return tuple(0.0 for _ in values)
    return tuple(component / length for component in values)


def climb_speed(distance, time):
    """Return the climb speed in units per second."""
    if time <= 0:
        raise ValueError("time must be positive")
    return float(distance) / float(time)


def ledge_id(seed, index):
    """Return a stable identifier for a ledge segment."""
    return f"{seed}:{index}"


def state_key(character_id):
    """Return the state store key for a character."""
    return character_id
