#Clean Transform
import maya.cmds as cmds


def transform_cleaner(lock, shapes, parent, shader):
    """
    Cleans the transform attributtes locking them, cleaning shapes, adding default shader and parent to the world.
    param: lock bool
    param: shapes bool
    param: parent: bool
    param: shader bool
    """
    trasnform_selcted_list = cmds.ls(sl=True, type='transform')
    if len(trasnform_selcted_list) < 1:
        cmnds.warning('Select at least one object!')
    else:
        for geo in trasnform_selcted_list:
            if lock:
            #Unlock transform
                cmds.setAttr('{}.v'.format(geo), lock=False, keyable=True)
                for attr in 'trs':
                    for axis in 'xyz':
                        cmds.setAttr('{}.{}{}'.format(geo, attr, axis), lock=False, keyable=True)
                #Display type 0 geo
                cmds.setAttr('{}.overrideEnabled'.format(geo), 0)
                cmds.setAttr('{}.overrideDisplayType'.format(geo), 0)
            if shapes:
                #Clean shapes ni=delete
                shapes_list = cmds.listRelatives(geo, shapes=True)
                if shapes_list:
                    for shape in shapes_list:
                        shape_ni_info = cmds.getAttr('{}.intermediateObject'.format(shape))
                    if shape_ni_info:
                        shape_orig = cmds.rename(shape, '{}ShapeOrig'.format(geo))
                        cmds.delete(shape_orig)
                    else:
                        shape = cmds.rename(shape, '{}Shape'.format(geo))
                        #Display type 0 shape
                        cmds.setAttr('{}.overrideEnabled'.format(shape), 0)
                        cmds.setAttr('{}.overrideDisplayType'.format(shape), 0)
                        cmds.setAttr('{}.displayEdges'.format(shape), 0)
                        cmds.setAttr('{}.displayColors'.format(shape), 0)
                        cmds.setAttr('{}.displayColorChannel'.format(shape), 'Ambient+Diffuse', type = 'string')
            if parent:
                cmds.parent(geo, absolute=True, world=True)
            #Clean history
            cmds.delete(geo, ch=True)
            #Add shader
            if shader:
                cmds.sets(edit=True, forceElement='initialShadingGroup')
