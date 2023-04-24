from maya import cmds
from maya_lib.libs import usage_lib, side_lib, math_lib, module_lib, control_lib
import importlib
importlib.reload(control_lib)


def build_spine(pelvis_guide, chest_guide, joint_number):
    """
    Get curve data
    :param chest_guide: str
    :param pelvis_guide: str
    :param joint_number: int
    """
    spine_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(module_lib.spine,
                                                                      module_lib.systems.capitalize()[:-1],
                                                                      side_lib.center, usage_lib.group))
    cmds.parent(spine_grp, 'bodySystem_c_grp')
    # Distance between  pelvis and chest
    distance_jnt = math_lib.distance_from_a_to_b(pelvis_guide, chest_guide)
    move_x = 0
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
        cmds.move(move_x, 0, 0, spine_node, objectSpace=True)
        if move_x < 1:
            move_x = distance_jnt/(joint_number-1)
        previous_spine = spine_node
    # Parent into skeleton grp
    cmds.parent(spine_list[0], 'skeleton_c_grp')  # Replace the group with a variable
    # Create iks
    iks_node, eff_node, iks_curve = cmds.ikHandle(startJoint=spine_list[0], endEffector=spine_list[-1],
                                                  name='{}_{}_{}'.format(module_lib.spine,
                                                                         spine_list[0].split('_')[1],
                                                                         usage_lib.ik_spline),
                                                  solver='ikSplineSolver', createCurve=True, simplifyCurve=True)
    cmds.rename(eff_node, '{}_{}_{}'.format(module_lib.spine, side_lib.center, usage_lib.effector))
    iks_curve = cmds.rename(iks_curve, '{}_{}_{}'.format(module_lib.spine, side_lib.center, usage_lib.effector))
    cmds.parent(iks_node, iks_curve, spine_grp)
    # Create control
    pelvis_control = control_lib.build_control(module_lib.pelvis, side_lib.center, 'circle')
