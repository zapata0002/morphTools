import maya.cmds as mc


def makeControlShape(transform, shape_type, color_name, scale=1):
    """
    :param transform: ctr
    :param shape_type: str
    :param color_name: int
    :param scale: int
    """
    if shape_type == "circle":
        # Build circle shape
        temp_ctrl = mc.circle(name="{}_CTRL".format(shape_type), degree=3, sections=8, normal=(0, 1, 0))[0]
    elif shape_type == "triangle":
        temp_ctrl = mc.circle(name="{}_CTRL".format(shape_type), degree=1, sections=3, normal=(0, 1, 0))[0]
    elif shape_type == "square":
        temp_ctrl = mc.curve(name="{}_CTRL".format(shape_type), degree=1,
                             point=[(-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1)])




    # Parent shapes to transform
    ctrl_shapes = mc.listRelatives(temp_ctrl, shapes=True)
    for i, shp in enumerate(ctrl_shapes):
        mc.parent(shp, transform, shape=True, relative=True)
        # Rename shapes
        if i == 0:
            new_shp_name = "{}Shape".format(transform)
        else:
            new_shp_name = "{}Shape{}".format(transform, i)
        mc.rename(shp, new_shp_name)
        # Scale shapes
        mc.scale(scale, scale, scale, "{}.cv[*]".format(transform))
        # Delete temp ctrl
        mc.delete(temp_ctrl)
    return transform

