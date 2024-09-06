import maya.cmds as mc


def unlock_node(node_list, translate=True, rotate=True, scale=True):
    """
    Unlock the transform translate, rotate, scale.
    param: transform_list: list
    param: translate: bool
    param: rotate: bool
    param: scale: bool
    """
    print(node_list)
    for node in node_list:
        print(node)
        # Unlock transform
        mc.setAttr('{}.v'.format(node), lock=False, keyable=True)
        for attr in ["translate", "rotate", "scale"]:
            for axis in "xyz":
                mc.setAttr("{}.{}{}".format(node, attr, axis), lock=False, keyable=True)


def clean_duplicate_shapes(geo_list):
    """
    Clean duplicate shapes
    """
    for obj in geo_list:
        print("{} processing".format(obj))

        # List all shapes related to the geometry
        shapes_list = mc.listRelatives(obj, shapes=True, fullPath=True)

        if shapes_list:
            print("{} Shapes: {}".format(obj, ', '.join(shapes_list)))

            original_shape = None

            for shape in shapes_list:
                # Check if the shape is set as intermediate
                is_intermediate = mc.getAttr("{}.intermediateObject".format(shape))

                if is_intermediate:
                    # Keep the original shape
                    original_shape = shape
                    shape = mc.rename(shape, '{}Shape'.format(obj))
                    print("{} kept as original shape".format(shape))
                    # Display type 0 shape
                    mc.setAttr('{}.overrideEnabled'.format(shape), 0)
                    mc.setAttr('{}.overrideDisplayType'.format(shape), 0)
                    mc.setAttr('{}.displayEdges'.format(shape), 0)
                    mc.setAttr('{}.displayColors'.format(shape), 0)
                    mc.setAttr('{}.displayColorChannel'.format(shape), 'Ambient+Diffuse', type='string')

                else:
                    # Delete intermediate shapes
                    mc.delete(shape)
                    print("{} deleted (intermediate object)".format(shape))

            if not original_shape:
                mc.warning("No original shape found for {}.".format(obj))

        else:
            mc.warning("{} does not contain any shapes. Make sure the selected node is a mesh.".format(obj))


def geo_cleaner(geo_list, unlock, shapes, parent, shader):
    """
    Cleans the transform attributtes locking them, cleaning shapes, adding default shader and parent to the world.
    param: geo_list: list
    param: unlock: bool
    param: shapes: bool
    param: parent: bool
    param: shader: bool
    """
    if len(geo_list) < 1:
        mc.warning('Select at least one object!')
    else:
        for geo in geo_list:
            if unlock:
                unlock_node(geo, translate=True, rotate=True, scale=True)
                #Display type 0 geo
                mc.setAttr('{}.overrideEnabled'.format(geo), 0)
                mc.setAttr('{}.overrideDisplayType'.format(geo), 0)
            if shapes:
                clean_duplicate_shapes(geo)
            if parent:
                mc.parent(geo, absolute=True, world=True)
            #Clean history
            mc.delete(geo, ch=True)
            #Add shader
            if shader:
                mc.sets(edit=True, forceElement='initialShadingGroup')

geo_cleaner(geo_list=mc.ls(sl=True), unlock=True, shapes=True, parent=True, shader=True)