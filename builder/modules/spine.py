# Imports
import importlib
from maya import cmds
from maya_lib.libs import usage_lib, side_lib, math_lib, module_lib, control_lib, connection_lib, curve_lib

importlib.reload(control_lib)


def build_spine(pelvis_guide, chest_guide, fk_controls, joint_number):
    """
    Get curve data
    :param chest_guide: str
    :param pelvis_guide: str
    :param fk_controls: str
    :param joint_number: int
    """
    spine_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.spine,
                                                                      module_lib.systems.capitalize()[:-1],
                                                                      side_lib.center, usage_lib.group))
    cmds.parent(spine_grp, 'bodySystem_c_grp')
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
    cmds.parent(spine_list[0], 'skeleton_c_grp')  # Replace the group with a variable
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
            (cmds.parent(spine_fk_zero, previous_fk_control))
        cmds.move(0, move_spine_fk_y, 0, spine_fk_zero, objectSpace=True)
        spine_fk_controls.append(spine_fk_control)
        spine_fk_zeros.append(spine_fk_zero)
        previous_fk_control = spine_fk_control
        if move_spine_fk_y < 1:
            move_spine_fk_y = distance_pelvis_chest/(fk_controls-0.5)
    cmds.xform(spine_fk_zeros[0], matrix=pelvis_matrix, worldSpace=True)
    cmds.parent(spine_fk_zeros[0], 'controls_c_grp')  # Replace the group with a variable
    # Create pelvis control and joint
    pelvis_control, pelvis_zero = control_lib.build_control(module_lib.pelvis, side_lib.center, 'circle', 5)
    pelvis_joint = cmds.createNode('joint', name='{}_{}_{}'.format(module_lib.pelvis, side_lib.center, usage_lib.curve_skin_joint))
    # Move by matrix the control and joint to the guide position
    cmds.xform(pelvis_control, matrix=pelvis_matrix, worldSpace=True)
    cmds.xform(pelvis_joint, matrix=pelvis_matrix, worldSpace=True)
    connection_lib.create_parent_constraint(pelvis_control, pelvis_joint)
    cmds.parent(pelvis_zero, 'controls_c_grp')  # Replace the group with a variable
    cmds.parent(pelvis_joint, 'skeleton_c_grp')  # Replace the group with a variable
    # Create chest control and joint
    chest_control, chest_zero = control_lib.build_control(module_lib.chest, side_lib.center, 'circle', 5)
    chest_joint = cmds.createNode('joint', name='{}_{}_{}'.format(module_lib.chest, side_lib.center, usage_lib.curve_skin_joint))
    # Move by matrix the control and joint to the guide position
    cmds.xform(chest_control, matrix=chest_matrix, worldSpace=True)
    cmds.xform(chest_joint, matrix=chest_matrix, worldSpace=True)
    connection_lib.create_parent_constraint(chest_control, chest_joint)
    cmds.parent(chest_zero, 'controls_c_grp')  # Replace the group with a variable
    cmds.parent(chest_joint, 'skeleton_c_grp')  # Replace the group with a variable

    spine_skin = cmds.skinCluster(pelvis_joint, chest_joint, spine_crv,
                                  name='{}{}_{}_{}'.format(spine_crv.split('_')[0],
                                                           spine_crv.split('_')[2].capitalize(),
                                                           spine_crv.split('_')[1], usage_lib.skin_cluster))[0]
    cmds.skinPercent(spine_skin, '{}.cv[:1]'.format(spine_crv), transformValue=(pelvis_joint, 1))
    cmds.skinPercent(spine_skin, '{}.cv[2:3]'.format(spine_crv), transformValue=(chest_joint, 1))
    # Stretch system
    curve_lib.stretch_curve(spine_crv, spine_list)
    connection_lib.create_parent_constraint(spine_fk_controls[-1], chest_zero)
