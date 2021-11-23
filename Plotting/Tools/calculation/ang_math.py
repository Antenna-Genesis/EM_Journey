import numpy as np


def wrapto180(ang_deg):
    # matrix_shape = np.shape(ang_deg)
    # map the angles into interval of [0, 360]
    angle = ang_deg % 360
    # force into the minimum absolute value residue class, so that -180 < angle <= 180
    angle[np.where(angle > 180)] -= 360
    return angle


def rad2deg(ang_rad):
    ang_deg = ang_rad * 180 / np.pi
    return ang_deg


def deg2rad(ang_deg):
    ang_rad = ang_deg * np.pi / 180
    return ang_rad
