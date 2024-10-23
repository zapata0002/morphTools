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


def reset_control_to_default(control_list=[], translate=True, rotate=True, scale=True, extras=False):
    """
    Reset controls to default
    param: control_list: list of strings
    param: translate: bool
    param: rotate: bool
    param: scale: bool
    param: extras: bool
    """
    for ctrl in control_list:
        print(ctrl)
        # Check attributes on the channelBox
        attrList = mc.listAttr(ctrl, unlocked=False, keyable=True, visible=True)
        for attr in attrList:
            if translate and attr.startswith("translate"):
                # Check if the attribute has input connection
                # cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                # if cnn_list:
                #    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                # else:
                # Get attribute default value
                value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                current_value = mc.attributeQuery(attr, node=ctrl, lisTdefault=False)[0]
                if value is not current_value:
                    # Set attribute to default
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
                else:
                    pass
            elif rotate and attr.startswith("rotate"):
                # Check if the attribute has input connection
                # cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                # if cnn_list:
                #    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                # else:
                # Get attribute default value
                value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                current_value = mc.attributeQuery(attr, node=ctrl, lisTdefault=False)[0]
                if value is not current_value:
                    # Set attribute to default
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
                else:
                    pass
            elif scale and attr.startswith("scale"):
                # Check if the attribute has input connection
                # cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                # if cnn_list:
                #    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                # else:
                # Get attribute default value
                value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                current_value = mc.attributeQuery(attr, node=ctrl, lisTdefault=False)[0]
                if value is not current_value:
                    # Set attribute to default
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
                else:
                    pass
            elif extras and not (attr.startswith("translate") or attr.startswith("rotate") or attr.startswith("scale")):
                # Check if the attribute has input connection
                # cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                # if cnn_list:
                #    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                # else:
                # Get attribute default value
                value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                current_value = mc.attributeQuery(attr, node=ctrl, lisTdefault=False)[0]
                if value is not current_value:
                    # Set attribute to default
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
                else:
                    pass
            else:
                pass

def reset_translate(control_list):
    """
    Reset translate to default
    param: control_list: list of strings
    """
    for ctrl in control_list:
        print(ctrl)
        # Check attributes on the channelBox
        attrList = mc.listAttr(ctrl, unlocked=False, keyable=True, visible=True)
        for attr in attrList:
            # Check if the attribute has input connection
            # cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
            # if cnn_list:
            #    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
            # else:
            # Get attribute default value
            value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
            current_value = mc.getAttr("{}.{}".format(ctrl, attr))
            if value is not current_value:
                # Set attribute to default
                mc.setAttr('{}.{}'.format(ctrl, attr), value)
                print(attr + " value --> " + str(value) + " current value --> " + str(current_value))
            else:
                pass
