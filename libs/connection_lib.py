import maya.cmds as cmds
from maya_lib.libs import usage_lib


def connect_3_axis(driver, driven, attr):
    """
    Connect attribute's X, Y and Z
    :param driver: str
    :param driven: str
    :param attr: str
    """
    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr('{}.{}{}'.format(driver, attr, axis), '{}.{}{}'.format(driven, attr, axis), force=True)


def connect_translate(driver, driven):
    """
    Connect translate
    :param driver: str
    :param driven: str
    """
    connect_3_axis(driver, driven, 'translate')


def connect_rotate(driver, driven):
    """
    Connect rotation
    :param driver: str
    :param driven: str
    """
    connect_3_axis(driver, driven, 'rotate')


def connect_scale(driver, driven):
    """
    Connect scale
    :param driver: str
    :param driven: str
    """
    connect_3_axis(driver, driven, 'scale')


def connect_translate_rotate_scale(driver, driven):
    """
    Connect translate, rotate and scale
    :param driver: str
    :param driven: str
    """
    connect_translate(driver, driven)
    connect_rotate(driver, driven)
    connect_scale(driver, driven)


def format_constraint_name(driven, usage):
    """
    Get constraint's name
    :param driven: str
    :param usage: str
    :return: constraint's name
    """
    node_desc, node_side, node_usage = driven.split('_')
    return '{}{}_{}_{}'.format(node_desc, node_usage.capitalize(), node_side, usage)


def create_parent_constraint(driver, driven, *args, **kwargs):
    """
    Create a parent constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: parent constraint
    """
    return cmds.parentConstraint(driver,
                                 driven,
                                 name=format_constraint_name(driven, usage_lib.parent_constraint), maintainOffset=True,
                                 *args, **kwargs)


def create_orient_constraint(driver, driven, *args, **kwargs):
    """
    Create a orient constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: orient constraint
    """
    cns = cmds.orientConstraint(driver,
                                driven,
                                name=format_constraint_name(driven, usage_lib.orient_constraint),
                                *args, **kwargs)
    return cns[0]


def create_point_constraint(driver, driven, *args, **kwargs):
    """
    Create a point constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: point constraint
    """
    cns = cmds.pointConstraint(driver,
                               driven,
                               name=format_constraint_name(driven, usage_lib.point_constraint),
                               *args, **kwargs)
    return cns[0]


def create_scale_constraint(driver, driven, *args, **kwargs):
    """
    Create a scale constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: scale constraint
    """
    cns = cmds.scaleConstraint(driver,
                               driven,
                               name=format_constraint_name(driven, usage_lib.scale_constraint),
                               *args, **kwargs)
    return cns[0]


def create_aim_constraint(driver, driven, *args, **kwargs):
    """
    Create a aim constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: aim constraint
    """
    cns = cmds.aimConstraint(driver,
                             driven,
                             name=format_constraint_name(driven, usage_lib.aim_constraint),
                             *args, **kwargs)
    return cns[0]


def create_pole_constraint(driver, driven, *args, **kwargs):
    """
    Create a pole vector constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: pole vector constraint
    """
    cns = cmds.poleVectorConstraint(driver,
                                    driven,
                                    name=format_constraint_name(driven, usage_lib.pole_vector_constraint),
                                    *args, **kwargs)
    return cns[0]
