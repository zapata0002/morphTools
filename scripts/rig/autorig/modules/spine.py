# Imports
import importlib
from maya import cmds
from maya_lib.libs import usage_lib, side_lib, math_lib, module_lib, control_lib, connection_lib, curve_lib, \
    deformer_lib, attribute_lib

importlib.reload(control_lib)
importlib.reload(usage_lib)


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
                                                    name='{}Ik_{}_{}'.format(module_lib.spine,
                                                                             spine_list[0].split('_')[1],
                                                                             usage_lib.ik_spline),
                                                    solver='ikSplineSolver', createCurve=True, simplifyCurve=True)
    cmds.rename(spine_eff, '{}_{}_{}'.format(module_lib.spine, side_lib.center, usage_lib.effector))
    spine_crv = cmds.rename(spine_crv, '{}_{}_{}'.format(module_lib.spine, side_lib.center, usage_lib.curve))
    cmds.parent(spine_iks, spine_crv, spine_grp)
    # Create cog control
    cog_control, cog_zero = control_lib.build_control(module_lib.cog, side_lib.center, 'fourPrisms', 2.5, 'green')
    cmds.xform(cog_zero, matrix=pelvis_matrix, worldSpace=True)
    cmds.parent(cog_zero, center_ctr)
    # Create spine FK controls
    move_spine_fk_y = 0
    previous_fk_control = None
    spine_fk_controls = []
    spine_fk_zeros = []
    for index in range(fk_controls):
        spine_fk_control, spine_fk_zero = control_lib.build_control('{}Fk{:02d}'.format(module_lib.spine, index+1),
                                                                    side_lib.center, 'spineFk', 1.5, 'yellow')
        if previous_fk_control:
            cmds.parent(spine_fk_zero, previous_fk_control)
        cmds.move(0, move_spine_fk_y, 0, spine_fk_zero, objectSpace=True)
        spine_fk_controls.append(spine_fk_control)
        spine_fk_zeros.append(spine_fk_zero)
        previous_fk_control = spine_fk_control
        if move_spine_fk_y < 1:
            move_spine_fk_y = distance_pelvis_chest/(fk_controls-0.5)
    cmds.xform(spine_fk_zeros[0], matrix=pelvis_matrix, worldSpace=True)
    cmds.parent(spine_fk_zeros[0], cog_control)
    # Create pelvis control and joint
    pelvis_control, pelvis_zero = control_lib.build_control(module_lib.pelvis, side_lib.center, 'pelvis', 1.75, 'yellow')
    pelvis_joint, pelvis_joint_zero = deformer_lib.build_joint(pelvis_control, usage_lib.skin_joint, True)
    # Move by matrix the control pelvis and joint to the guide position
    cmds.xform(pelvis_zero, matrix=pelvis_matrix, worldSpace=True)
    cmds.xform(pelvis_joint_zero, matrix=pelvis_matrix, worldSpace=True)
    connection_lib.create_parent_constraint(pelvis_control, pelvis_joint)
    cmds.parent(pelvis_zero, cog_control)
    cmds.parent(pelvis_joint_zero, skeleton_grp)
    # Create chest control and joint
    chest_control, chest_zero = control_lib.build_control(module_lib.chest, side_lib.center, 'circle', 2.5, 'green')
    chest_joint, chest_joint_zero = deformer_lib.build_joint(chest_control, usage_lib.skin_joint, True)
    chest_attr = attribute_lib.Helper(chest_control)
    chest_attr.add_separator_attribute('Attributes')
    chest_attr = chest_attr.add_float_attribute('autoSquash', minValue=0, maxValue=1, defaultValue=1)
    # Move by matrix the chest control and joint to the guide position
    cmds.xform(chest_zero, matrix=chest_matrix, worldSpace=True)
    cmds.xform(chest_joint_zero, matrix=chest_matrix, worldSpace=True)
    connection_lib.create_parent_constraint(chest_control, chest_joint)
    cmds.parent(chest_zero, cog_control)
    cmds.parent(chest_joint_zero, skeleton_grp)
    # Clusters ik spine
    pelvis_cluster, pelvis_cluster_handle = cmds.cluster('{}.cv[:1]'.format(spine_crv))
    cmds.rename(pelvis_cluster, '{}_{}_{}'.format(module_lib.pelvis, side_lib.center,
                                                  usage_lib.cluster))
    pelvis_cluster_handle = cmds.rename(pelvis_cluster_handle, '{}_{}_{}'.format(module_lib.pelvis,
                                                                                 side_lib.center,
                                                                                 usage_lib.cluster_handle))
    connection_lib.create_parent_constraint(pelvis_control, pelvis_cluster_handle)
    chest_cluster, chest_cluster_handle = cmds.cluster('{}.cv[2:]'.format(spine_crv))
    cmds.rename(chest_cluster, '{}_{}_{}'.format(module_lib.chest, side_lib.center,
                                                 usage_lib.cluster))
    chest_cluster_handle = cmds.rename(chest_cluster_handle, '{}_{}_{}'.format(module_lib.chest, side_lib.center,
                                                                               usage_lib.cluster_handle))
    connection_lib.create_parent_constraint(chest_control, chest_cluster_handle)
    cmds.parent(pelvis_cluster_handle, chest_cluster_handle, spine_grp)
    # Stretch system
    global_norm_node = curve_lib.stretch_curve(spine_crv, spine_list)
    connection_lib.create_parent_constraint(spine_fk_controls[-1], chest_zero)
    cmds.connectAttr('{}.globalScale'.format(general_ctr), '{}GlobalScale_{}_{}.input2.input2X'.format(module_lib.spine,
                                                                                                       side_lib.center,
                                                                                                       usage_lib.norm))
    # Squash system
    bc_node = curve_lib.auto_squash(spine_list[:-1], module_lib.spine)
    cmds.connectAttr('{}.output.outputX'.format(global_norm_node), '{}.color1.color1R'.format(bc_node))
    cmds.connectAttr('{}.{}'.format(chest_control, chest_attr), '{}.blender'.format(bc_node))
    # Spine middle ik
    middle_spine_control, middle_spine_zero = control_lib.build_control(module_lib.middle_spine, side_lib.center,
                                                                        'circle', 1.5, 'green')
    spine_middle_position = math_lib.middle_point(cmds.exactWorldBoundingBox([pelvis_guide, chest_guide]))
    cmds.xform(middle_spine_zero, translation=spine_middle_position, worldSpace=True)
    cmds.parent(middle_spine_zero, cog_control)
    # Spine bend curve
    bend_curve = cmds.duplicate(spine_crv, name='{}Bend_{}_{}'.format(module_lib.spine, side_lib.center,
                                                                      usage_lib.curve))[0]
    cmds.delete(cmds.listRelatives(bend_curve, shapes=True)[-1])
    up_bend_cluster, up_bend_cluster_handle = cmds.cluster('{}.cv[1]'.format(bend_curve))
    cmds.rename(up_bend_cluster, 'up{}Bend_{}_{}'.format(module_lib.spine.capitalize(),
                                                         side_lib.center,
                                                         usage_lib.cluster))
    up_bend_cluster_handle = cmds.rename(up_bend_cluster_handle,
                                         'up{}Bend_{}_{}'.format(module_lib.spine.capitalize().capitalize(),
                                                                 side_lib.center,
                                                                 usage_lib.cluster_handle))
    dw_bend_cluster, dw_bend_cluster_handle = cmds.cluster('{}.cv[2]'.format(bend_curve))
    cmds.rename(dw_bend_cluster, 'dw{}Bend_{}_{}'.format(module_lib.spine.capitalize().capitalize(),
                                                         side_lib.center,
                                                         usage_lib.cluster))
    dw_bend_cluster_handle = cmds.rename(dw_bend_cluster_handle,
                                         'dw{}Bend_{}_{}'.format(module_lib.spine.capitalize().capitalize(),
                                                                 side_lib.center,
                                                                 usage_lib.cluster_handle))
    connection_lib.connect_translate(middle_spine_control, up_bend_cluster_handle)
    connection_lib.connect_translate(middle_spine_control, dw_bend_cluster_handle)
    cmds.parent(up_bend_cluster_handle, dw_bend_cluster_handle, spine_grp)
    cmds.blendShape(bend_curve, spine_crv, name='{}_{}'.format(spine_crv, usage_lib.blend_shape),
                    weight=(0, 1.0), frontOfChain=True)
    cmds.setAttr('{}.visibility'.format(spine_grp), 0)
