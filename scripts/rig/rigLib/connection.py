import maya.cmds as mc


def connect_translate(driver, driven):
    """
    Connect translation from A to B
    :param driver: string
    :param driven: string
    """
    for axis in "XYZ":
        mc.connectAttr("{}.translate.translate{}".format(driver, axis),
                       "{}.translate.translate{}".format(driven, axis))


def connect_rotate(driver, driven):
    """
    Connect rotation from A to B
    :param driver: string
    :param driven: string
    """
    for axis in "XYZ":
        mc.connectAttr("{}.rotate.rotate{}".format(driver, axis),
                       "{}.rotate.rotate{}".format(driven, axis))


def connect_scale(driver, driven):
    """
    Connect scale from A to B
    :param driver: string
    :param driven: string
    """
    for axis in "XYZ":
        mc.connectAttr("{}.rotate.rotate{}".format(driver, axis),
                       "{}.rotate.rotate{}".format(driven, axis))


def connect_translate_rotate_scale(driver, driven):
    """
    Connect translation, rotation and scale from A to B
    :param driver: string
    :param driven: string
    """
    for attr in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            mc.connectAttr("{}.{}.{}{}".format(driver, attr, attr, axis),
                           "{}.{}.{}{}".format(driven, attr, attr, axis))


