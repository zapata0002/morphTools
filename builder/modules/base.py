from maya import cmds
from maya_lib.libs import usage_lib, side_lib, module_lib, control_lib, attribute_lib
import importlib
importlib.reload(attribute_lib)


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
    general_control, general_zero = control_lib.build_control(module_lib.general, side_lib.center, 'circle', 10)
    general_helper = attribute_lib.Helper(general_control)
    general_helper.global_scale_attribute()
    center_control, center_zero = control_lib.build_control(module_lib.center, side_lib.center, 'circle', 8)
    cmds.parent(center_zero, general_control)
    cmds.parent(general_zero, controls_grp)
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

