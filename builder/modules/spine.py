# Imports
import importlib
from maya import cmds
from maya_lib.libs import usage_lib, side_lib, math_lib, module_lib, control_lib, connection_lib, curve_lib, \
    deformer_lib, attribute_lib

importlib.reload(curve_lib)


def build_spine(pelvis_guide, chest_guide, fk_controls, joint_number):
    """
    Get curve data
    :param chest_guide: str
    :param pelvis_guide: str
    :param fk_controls: str
    :param joint_number: int
    """
    # Basic groups for the spine
    body_grp = '{}{}_{}_{}'.format(module_lib.body, module_lib.system.capitalize(), side_lib.center, usage_lib.group)
    skeleton_grp = '{}_{}_{}'.format(module_lib.skeleton, side_lib.center, usage_lib.group)
    general_ctr = '{}_{}_{}'.format(module_lib.general, side_lib.center, usage_lib.control)
    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr('{}.globalScale'.format(general_ctr),
                         '{}.scale.scale{}'.format(skeleton_grp, axis),
                         force=True)
    center_ctr = '{}_{}_{}'.format(module_lib.center, side_lib.center, usage_lib.control)
    spine_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.spine,
                                                                      module_lib.system.capitalize(),
                                                                      side_lib.center, usage_lib.group))
    cmds.parent(spine_grp, body_grp)
    pelvis_matrix = cmds.xform(pelvis_guide, query=True, matrix=True, worldSpace=True)
    chest_matrix = cmds.xform(chest_guide, query=True, matrix=True, worldSpace=True)
    # Distance between  pelvis and chest
    distance_pelvis_chest = math_lib.distance_from_a_to_b(pelvis_guide, chest_guide)
    move_spine_x = 0
    previous_spine = None
    spine_list = []
    # Spine joints
    for index in range(joint_number):
        spine_node = cmds.createNode('joint', name='{}{:02d}_{}_{}'.format(module_lib.spine, index+1, side_lib.center,
                                                                           usage_lib.skin_joint))
        cmds.setAttr('{}.jointOrientZ'.format(spine_node), 90)
        spine_list.append(spine_node)
        if previous_spine:
            cmds.parent(spine_node, previous_spine)
        cmds.move(move_spine_x, 0, 0, spine_node, objectSpace=True)
        if move_spine_x < 1:
            move_spine_x = distance_pelvis_chest/(joint_number-1)
        previous_spine = spine_node
    pelvis_translation = cmds.xform(pelvis_guide, query=True, translation=True, worldSpace=True)
    cmds.xform(spine_list[0], translation=pelvis_translation, worldSpace=True)
    # Parent into skeleton grp
    cmds.parent(spine_list[0], skeleton_grp)
    # Create spine ik spline
    spine_iks, spine_eff, spine_crv = cmds.ikHandle(startJoint=spine_list[0], endEffector=spine_list[-1],
                                                    name='{}_{}_{}'.format(module_lib.spine,
                                                                           spine_list[0].split('_')[1],
                                                                           usage_lib.ik_spline),
                                                    solver='ikSplineSolver', createCurve=True, simplifyCurve=True)
    cmds.rename(spine_eff, '{}_{}_{}'.format(module_lib.spine, side_lib.center, usage_lib.effector))
    spine_crv = cmds.rename(spine_crv, '{}_{}_{}'.format(module_lib.spine, side_lib.center, usage_lib.curve))
    cmds.parent(spine_iks, spine_crv, spine_grp)
    # Create spine FK controls
    move_spine_fk_y = 0
    previous_fk_control = None
    spine_fk_controls = []
    spine_fk_zeros = []
    for index in range(fk_controls):
        spine_fk_control, spine_fk_zero = control_lib.build_control('{}Fk{:02d}'.format(module_lib.spine, index+1),
                                                                    side_lib.center, 'square', 3)
        if previous_fk_control:
            cmds.parent(spine_fk_zero, previous_fk_control)
        cmds.move(0, move_spine_fk_y, 0, spine_fk_zero, objectSpace=True)
        spine_fk_controls.append(spine_fk_control)
        spine_fk_zeros.append(spine_fk_zero)
        previous_fk_control = spine_fk_control
        if move_spine_fk_y < 1:
            move_spine_fk_y = distance_pelvis_chest/(fk_controls-0.5)
    cmds.xform(spine_fk_zeros[0], matrix=pelvis_matrix, worldSpace=True)
    cmds.parent(spine_fk_zeros[0], center_ctr)
    # Create pelvis control and joint
    pelvis_control, pelvis_zero = control_lib.build_control(module_lib.pelvis, side_lib.center, 'allDirections3D', 5)
    pelvis_joint, pelvis_joint_zero = deformer_lib.build_joint(pelvis_control, usage_lib.skin_joint, True)
    # Move by matrix the control and joint to the guide position
    cmds.xform(pelvis_zero, matrix=pelvis_matrix, worldSpace=True)
    cmds.xform(pelvis_joint_zero, matrix=pelvis_matrix, worldSpace=True)
    connection_lib.create_parent_constraint(pelvis_control, pelvis_joint)
    cmds.parent(pelvis_zero, center_ctr)
    cmds.parent(pelvis_joint_zero, skeleton_grp)
    # Create chest control and joint
    chest_control, chest_zero = control_lib.build_control(module_lib.chest, side_lib.center, 'circle', 5)
    chest_joint, chest_joint_zero = deformer_lib.build_joint(chest_control, usage_lib.skin_joint, True)
    chest_helper = attribute_lib.Helper(chest_control)
    chest_helper.add_separator_attribute('attributes')
    chest_helper.add_float_attribute('autoSquash', minValue=0, maxValue=1, defaultValue=1)
    # Move by matrix the control and joint to the guide position
    cmds.xform(chest_zero, matrix=chest_matrix, worldSpace=True)
    cmds.xform(chest_joint_zero, matrix=chest_matrix, worldSpace=True)
    connection_lib.create_parent_constraint(chest_control, chest_joint)
    cmds.parent(chest_zero, center_ctr)
    cmds.parent(chest_joint_zero, skeleton_grp)

    spine_skin = cmds.skinCluster(pelvis_joint, chest_joint, spine_crv,
                                  name='{}{}_{}_{}'.format(spine_crv.split('_')[0],
                                                           spine_crv.split('_')[2].capitalize(),
                                                           spine_crv.split('_')[1], usage_lib.skin_cluster))[0]
    cmds.skinPercent(spine_skin, '{}.cv[:1]'.format(spine_crv), transformValue=(pelvis_joint, 1))
    cmds.skinPercent(spine_skin, '{}.cv[2:3]'.format(spine_crv), transformValue=(chest_joint, 1))
    # Stretch system
    curve_lib.stretch_curve(spine_crv, spine_list)
    connection_lib.create_parent_constraint(spine_fk_controls[-1], chest_zero)
    cmds.connectAttr('{}.globalScale'.format(general_ctr), '{}GlobalScale_{}_{}.input2.input2X'.format(module_lib.spine,
                                                                                                       side_lib.center,
                                                                                                       usage_lib.norm))
    # Squash system
    curve_lib.auto_squash(spine_list[:-1], module_lib.spine)
