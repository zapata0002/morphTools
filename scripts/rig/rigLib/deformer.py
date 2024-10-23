from maya import cmds as mc
import importlib



def build_joint(node, usage, zero):
    """
    Build joint
    :param node: str
    :param usage: str
    :param zero: boolean
    """
    joint_node = mc.createNode('joint', name='{}_{}_{}'.format(node.split('_')[0], node.split('_')[1], usage))
    if zero:
        joint_zero = mc.createNode('transform', name='{}{}_{}_{}'.format(node.split('_')[0], usage.capitalize(),
                                                                           node.split('_')[1], usage_lib.zero))
        mc.parent(joint_node, joint_zero)
        return joint_node, joint_zero
    else:
        return joint_node


# Select joints from geo
def select_joints(transform_list=[]):
    if len(transform_list) == 0:
        mc.warning('Select the geometry')
    if len(transform_list) == 1:
        for transform in transform_list:
            joint_list = []
            shape = mc.listRelatives(transform, shapes=True, noIntermediate=True)
            shape_history = mc.listHistory(shape)
            for node in shape_history:
                if mc.nodeType(node) == 'skinCluster':
                    joints_from_skin = mc.skinCluster(node, q=True, inf=True)
                    joint_list.extend(joints_from_skin)

        mc.select(joint_list)
        return joint_list


def select_joints_from_skin(skin_list):
    if len(skin_list) == 0:
        mc.warning('Select the geometry')
    if len(skin_list) >= 1:
        for skn in skin_list:
            bind_list = []
            if mc.nodeType(skn) != "skinCluster":
                mc.warning("You must select skinCluster node")
            else:
                joints_from_skin = mc.skinCluster(skn, q=True, inf=True)
                bind_list.extend(joints_from_skin)

        mc.select(bind_list)
    return bind_list


def generate_lable_joints(joint_list=[]):
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

#Rename deformers
# Check that the object name has "DESCRIPTOR_SIDE_USAGE"

def rename_deformers(transform_list=None):
    for node in transform_list:           
            if len(node) < 1:
                mc.warning('Select the geometry with deformers')
            if len(node) >= 1:
                nonLinear_types = {'deformBend': 'bend',
                                   'deformFlare': 'flare',
                                   'deformSine': 'sine',
                                   'deformSquash': 'squash',
                                   'deformTwist': 'twist',
                                   'deformWave': 'wave'}
                                   
                # Get the shape of the selected object
                shape = mc.listRelatives(transform_list, shapes=True, noIntermediate=True)
                # Get the skinClusters and blendShapes that are connected to the shape
                skin_list = mc.listConnections(shape, type='skinCluster')
                blendShape_list = mc.listConnections(shape, type='blendShape')
                # Rename the selected skinClusters and blendShapes
                for skin in skin_list:
                    mc.rename(skin, '{}_{}_skin'.format(skin.split('_')[0],
                                                          skin.split('_')[1]))
                for bs in blendShape_list:
                    mc.rename(bs, '{}_{}_bs'.format(bs.split('_')[0],
                                                        bs.split('_')[1]))


                history_nodes = mc.listHistory(shape, pdo=True)
                for history_node in history_nodes:
                    if 'geometryFilter' in mc.nodeType(history_node, i=True, d=False):
                        type = mc.nodeType(history_node)
                        if type == 'nonLinear':
                            deform_shape = mc.listConnections('{}.deformerData'.format(history_node), s=True, d=False, sh=True)
                            if not deform_shape:
                                continue
                            nonLinear_type = mc.nodeType(deform_shape[0])
                            if nonLinear_type not in nonLinear_types:
                                continue
                            type = nonLinear_types[nonLinear_type]
                        nodes_name = '{}_{}_{}'.format(node.split('_')[0], node.split('_')[1], type)
                        mc.rename(history_node, nodes_name)
                    else:
                        type = mc.nodeType(history_node, i=True, d=False)[0]
                        nodes_name = (node.split('_')[0], node.split('_')[1], type)

def rename_bind_poses():
    bind_pose_list = mc.ls(type='dagPose')
    if bind_pose_list:
        for bind_pose in bind_pose_list:
            skin_connections = mc.listConnections(bind_pose, type='skinCluster')
            if skin_connections:
                skin_node = skin_connections[0]
                bind_pose_name = '{}_bp'.format(skin_node)
                mc.rename(bind_pose, bind_pose_name)
    else:
        pass

def rename_unit_conversion():
    uc_list = mc.ls(type='unitConversion')
    if uc_list:
        for uc in uc_list:
            uc_connection = mc.listConnections('{}.output'.format(uc), plugs=True)
            uc_output = uc_connection[0]
            if len(uc_output.split('.')[0].split('_')) == 2:
                descriptor, side, usage = uc_output.split('.')[0].split('_')
                mc.rename(uc, '{}{}_{}_{}_bp'.format(descriptor, uc_output.split('.')[1].capitalize(), side, usage))
            else:
                mc.rename(uc, '{}{}_bp'.format(uc_output.split('.')[0], uc_output.split('.')[1].capitalize()))
    else:
        pass
