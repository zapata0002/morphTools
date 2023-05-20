from maya import cmds
from maya_lib.libs import usage_lib, side_lib, module_lib, control_lib, attribute_lib
import importlib
importlib.reload(module_lib)


def rig_base(asset_type):
    geo_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.geo, side_lib.center, usage_lib.group))
    rig_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.rig, side_lib.center, usage_lib.group))
    controls_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.controls, side_lib.center,
                                                                       usage_lib.group))
    systems_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.systems, side_lib.center,
                                                                      usage_lib.group))
    skeleton_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.skeleton, side_lib.center,
                                                                       usage_lib.group))
    cmds.parent(skeleton_grp, systems_grp)
    cmds.parent(controls_grp, systems_grp, rig_grp)
    general_control, general_zero = control_lib.build_control(module_lib.general, side_lib.center, 'general', 2.5,
                                                              'white')
    general_helper = attribute_lib.Helper(general_control)
    general_helper.global_scale_attribute()
    center_control, center_zero = control_lib.build_control(module_lib.center, side_lib.center, 'circle', 2.5, 'green')
    cmds.parent(center_zero, general_control)
    cmds.parent(general_zero, controls_grp)
    """
    # Create visibility control
    visibility_control, visibility_zero = control_lib.build_control(module_lib.visibility, side_lib.center, 'eye', 0.5,
                                                                    'white')
    cmds.move(0, 0, 3.7, visibility_zero)
    # Lock and hide attrs
    attributes_cb = ['{}.v'.format(visibility_control)]
    for attr in 'trs':
        for axis in 'XYZ':
            attribute = '{}.{}{}'.format(visibility_control, attr, axis)
            attributes_cb.append(attribute)
    print(attributes_cb)
    attribute_lib.lock_and_hide_attributes(attributes_cb , lock=True, hide=True)
    """
    # Add attributes
    # Set attrs
    if asset_type == 'char':
        asset_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.char, side_lib.center,
                                                                        usage_lib.group))
        body_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.body,
                                                                         module_lib.systems.capitalize()[:-1],
                                                                         side_lib.center, usage_lib.group))
        facial_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.facial,
                                                                           module_lib.systems.capitalize()[:-1],
                                                                           side_lib.center, usage_lib.group))
        cmds.parent(body_grp, facial_grp, systems_grp)
    if asset_type == 'prop':
        asset_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.prop, side_lib.center,
                                                                        usage_lib.group))
    if asset_type == 'set':
        asset_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.set, side_lib.center,
                                                                        usage_lib.group))
    cmds.parent(geo_grp, rig_grp, asset_grp)
    if asset_type == 'char':
        return asset_grp, geo_grp, rig_grp, controls_grp, systems_grp, skeleton_grp, body_grp, facial_grp
    else:
        return asset_grp, geo_grp, rig_grp, controls_grp, systems_grp, skeleton_grp
