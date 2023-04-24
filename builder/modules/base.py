from maya import cmds
from maya_lib.libs import usage_lib, side_lib, module_lib
import importlib
importlib.reload(module_lib)


def rig_base():
    all_grp = cmds.createNode('transform', name=module_lib.all)
    geo_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.geo, side_lib.center, usage_lib.group))
    rig_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.rig, side_lib.center, usage_lib.group))
    controls_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.controls, side_lib.center,
                                                                       usage_lib.group))
    systems_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.systems, side_lib.center,
                                                                      usage_lib.group))
    body_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.body,
                                                                     module_lib.systems.capitalize()[:-1],
                                                                     side_lib.center, usage_lib.group))
    facial_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.facial,
                                                                       module_lib.systems.capitalize()[:-1],
                                                                       side_lib.center, usage_lib.group))
    skeleton_grp = cmds.createNode('transform', name='{}_{}_{}'.format(module_lib.skeleton, side_lib.center,
                                                                       usage_lib.group))
    cmds.parent(body_grp, skeleton_grp, facial_grp, systems_grp)
    cmds.parent(controls_grp, systems_grp, rig_grp)
    cmds.parent(geo_grp, rig_grp, all_grp)
    return all_grp, geo_grp, rig_grp, controls_grp, systems_grp, body_grp, facial_grp
