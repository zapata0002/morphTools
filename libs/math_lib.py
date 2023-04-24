# Imports
import math
from maya import cmds


def distance_from_a_to_b(a, b):
    a_pos = cmds.xform(a, query=True, worldSpace=True, translation=True)
    b_pos = cmds.xform(b, query=True, worldSpace=True, translation=True)

    return float(math.dist(a_pos, b_pos))


def middle_point(bbox):
    x = (bbox[0] + bbox[3]) / 2.0
    y = (bbox[1] + bbox[4]) / 2.0
    z = (bbox[2] + bbox[5]) / 2.0
    pos = [x, y, z]
    return pos
