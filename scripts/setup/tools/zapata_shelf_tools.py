import maya.cmds as mc



def geo_cleaner(geo_list=[], lock=True, shapes=True, parent=True, shader=True):
    """
    Cleans the transform attributtes locking them, cleaning shapes, adding default shader and parent to the world.
    param: lock: bool
    param: shapes: bool
    param: parent: bool
    param: shader: bool
    """
    if len(geo_list) < 1:
        cmnds.warning('Select at least one object!')
    else:
        for geo in geo_list:
            if lock:
            #Unlock transform
                mc.setAttr('{}.v'.format(geo), lock=False, keyable=True)
                for attr in 'trs':
                    for axis in 'xyz':
                        mc.setAttr('{}.{}{}'.format(geo, attr, axis), lock=False, keyable=True)
                #Display type 0 geo
                mc.setAttr('{}.overrideEnabled'.format(geo), 0)
                mc.setAttr('{}.overrideDisplayType'.format(geo), 0)
            if shapes:
                #Clean shapes ni=delete
                shapes_list = mc.listRelatives(geo, shapes=True)
                if shapes_list:
                    for shape in shapes_list:
                        shape_ni_info = mc.getAttr('{}.intermediateObject'.format(shape))
                    if shape_ni_info:
                        shape_orig = mc.rename(shape, '{}ShapeOrig'.format(geo))
                        mc.delete(shape_orig)
                    else:
                        shape = mc.rename(shape, '{}Shape'.format(geo))
                        #Display type 0 shape
                        mc.setAttr('{}.overrideEnabled'.format(shape), 0)
                        mc.setAttr('{}.overrideDisplayType'.format(shape), 0)
                        mc.setAttr('{}.displayEdges'.format(shape), 0)
                        mc.setAttr('{}.displayColors'.format(shape), 0)
                        mc.setAttr('{}.displayColorChannel'.format(shape), 'Ambient+Diffuse', type = 'string')
            if parent:
                mc.parent(geo, absolute=True, world=True)
            #Clean history
            mc.delete(geo, ch=True)
            #Add shader
            if shader:
                mc.sets(edit=True, forceElement='initialShadingGroup')


def reset_controls(control_list=[], translate=True, rotate=True, scale=True, extras=True):
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
                cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)

                if cnn_list:
                    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                else:
                    # Get attribute default value
                    value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                    # Set attribute to default 
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
            elif rotate and attr.startswith("rotate"):
                cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                if cnn_list:
                    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                else:
                    value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
            elif scale and attr.startswith("scale"):
                cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                if cnn_list:
                    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                else:
                    value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
            elif extras and not (attr.startswith("translate") or attr.startswith("rotate") or attr.startswith("scale")):
                cnn_list = mc.listConnections("{}.{}".format(ctrl, attr), source=True, destination=False)
                if cnn_list:
                    mc.warning("Cannot reset to default {}.{}, it has an input connection".format(ctrl, attr))
                else:
                    value = mc.attributeQuery(attr, node=ctrl, listDefault=True)[0]
                    mc.setAttr('{}.{}'.format(ctrl, attr), value)
                    print(attr, value)
            else:
                pass

def lable_joints(joint_list=[]):
    for i, jnt in enumerate(joint_list):
        if "|" in jnt:
            temp_name = jnt.split("|")[-1]
            descriptor, side, usage = temp_name.split("_")
        else:
            descriptor, side, usage = jnt.split("_")
        if side in 'lL':
            mc.setAttr(jnt+".side", 1)
        elif side in 'rR':
            mc.setAttr(jnt+".side", 2)
        elif side in 'mM':
            mc.setAttr(jnt+".side", 0)
        else:
            mc.setAttr(jnt+".side", 3)
        # Set type to other
        mc.setAttr(jnt + ".type", 18)
        # Set other type
        mc.setAttr(jnt + ".otherType", descriptor, type="string")

def select_joints(joint_list=[]):
    for jnt in joint_list:
        print(jnt)
        mc.select(jnt)


def connect_local(driver, driven, translate=False, rotate=False, scale=False):
    """
    Connect translate, rotate and scale
    :param driver: str
    :param driven: str
    :param translate: bool
    :param rotate: bool
    :param scale: bool
    """
    if translate:
        for axis in ['X', 'Y', 'Z']:
            mc.connectAttr('{}.translate{}'.format(driver, axis), '{}.translate{}'.format(driven, axis), force=True)
            print("Connected {}.translate{} to {}.translate{}".format(driver, axis, driven, axis))
    if rotate:
        for axis in ['X', 'Y', 'Z']:
            mc.connectAttr('{}.rotate{}'.format(driver, axis), '{}.rotate{}'.format(driven, axis), force=True)
            print("Connected {}.rotate{} to {}.rotate{}".format(driver, axis, driven, axis))
    if scale:
        for axis in ['X', 'Y', 'Z']:
            mc.connectAttr('{}.scale{}'.format(driver, axis), '{}.scale{}'.format(driven, axis), force=True)
            print("Connected {}.scale{} to {}.scale{}".format(driver, axis, driven, axis))
    else:
        mc.connectAttr(mc.connectAttr('{}'.format(driver), '{}'.format(driven), force=True))
        print("Connected {} to {}".format(driver, driven))

def scene_cleaner(nodes):
    # Remove unused nodes on the scene
    unused_nodes = [
        "mayaUsdLayerManager", 
        "sequenceManager", 
        "script", 
        "shapeEditorManager", 
        "trackInfoManager", 
        "poseInterpolatorManager", 
        "blendShape", 
        "unknown", 
        "aiAOVDriver",
        "aiAOVFilter",
        "aiOptions"
    ]

    unused_list = mc.ls(type=unused_nodes)
    if not unused_list:
        print("No unused nodes in this scene")
    else:
        for node in unused_list:
            if node in ["sequenceManager", "shapeEditorManager", "poseInterpolatorManager"]:
                print(node + " node can not be remove in the scene.")
            else:
                try:
                    mc.delete(node)
                    print("Delete: " + node)
                except:
                    print("Deleted: " + node)