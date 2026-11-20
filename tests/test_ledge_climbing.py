import pytest
from gameplay import ledge_climbing as mod

CASES = [
    ("space", 'm.ledge_space(2, 1) is True'),
    ("hyst", 'm.state_hysteresis(0.5, 0.2) is True'),
    ("root", 'm.root_motion_offset((10, 0), (2, 0)) == (8, 0)'),
    ("occ", 'm.ledge_occupancy([1], 2) is True'),
    ("auth", 'm.authoritative_point((1, 0), (1, 1)) == (1, 1)'),
    ("event", 'm.animation_event_time(0.2, 0.5) is True'),
    ("slope", 'm.slope_normal((1, 1, 0)) == approx((0.707107, 0.707107, 0.0))'),
    ("cancel", 'm.cancel_velocity((2, 3)) == (0, 0)'),
    ("save", 'm.save_climb_state("climb", True) == "climb"'),
    ("layer", 'm.collision_layer(1, 0b0010) is False'),
    ("dist", 'm.grab_distance((0, 0), (3, 4)) == approx(5.0)'),
    ("normal", 'm.ledge_normal((0, 2, 0)) == (0, 1, 0)'),
    ("speed", 'm.climb_speed(10, 5) == approx(2.0)'),
    ("id", 'm.ledge_id(3, 2) == "3:2"'),
    ("key", 'm.state_key("p1") == "p1"')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
