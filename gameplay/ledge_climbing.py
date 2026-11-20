import math

def ledge_space(clearance, height):
    """ledge 上方净空。"""
    raise NotImplementedError("TODO: ledge_space")

def state_hysteresis(distance, threshold):
    """状态滞回。"""
    raise NotImplementedError("TODO: state_hysteresis")

def root_motion_offset(animation, climb):
    """攀爬根运动。"""
    raise NotImplementedError("TODO: root_motion_offset")

def ledge_occupancy(occupants, capacity):
    """ledge 占用。"""
    raise NotImplementedError("TODO: ledge_occupancy")

def authoritative_point(client_point, server_point):
    """服务器权威点。"""
    raise NotImplementedError("TODO: authoritative_point")

def animation_event_time(event_time, frame_time):
    """动画事件采样。"""
    raise NotImplementedError("TODO: animation_event_time")

def slope_normal(normal):
    """斜面法线投影。"""
    raise NotImplementedError("TODO: slope_normal")

def cancel_velocity(current):
    """取消清速度。"""
    raise NotImplementedError("TODO: cancel_velocity")

def save_climb_state(state, valid):
    """存档攀爬状态。"""
    raise NotImplementedError("TODO: save_climb_state")

def collision_layer(layer, climb_mask):
    """攀爬碰撞层。"""
    raise NotImplementedError("TODO: collision_layer")

def grab_distance(position, ledge):
    """抓取距离。"""
    raise NotImplementedError("TODO: grab_distance")

def ledge_normal(normal):
    """ledge 法线。"""
    raise NotImplementedError("TODO: ledge_normal")

def climb_speed(distance, time):
    """攀爬速度。"""
    raise NotImplementedError("TODO: climb_speed")

def ledge_id(seed, index):
    """ledge id。"""
    raise NotImplementedError("TODO: ledge_id")

def state_key(character_id):
    """状态键。"""
    raise NotImplementedError("TODO: state_key")
