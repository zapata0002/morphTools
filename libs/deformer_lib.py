from maya import cmds
import maya.cmds as cmds


def build_joint(node, usage):
    return cmds.createNode('joint', name='{}_{}_{}'.format(node.split('_')[0], node.split('_')[1], usage))


# Select joints from geo
def select_joints(transform_list=[]):
    if len(transform_list) == 0:
        cmds.warning('Select the geometry')
    if len(transform_list) == 1:
        for transform in transform_list:
            joint_list = []
            shape = cmds.listRelatives(transform, shapes=True, noIntermediate=True)
            shape_history = cmds.listHistory(shape)
            for node in shape_history:
                if cmds.nodeType(node) == 'skinCluster':
                    joints_from_skin = cmds.skinCluster(node, q=True, inf=True)
                    joint_list.extend(joints_from_skin)

        cmds.select(joint_list)

#Rename deformers
# Check that the object name has "DESCRIPTOR_SIDE_USAGE"

def rename_deformers(transform_list=None):
    for node in transform_list:           
            if len(node) < 1:
                cmds.warning('Select the geometry with deformers')
            if len(node) >= 1:
                nonLinear_types = {'deformBend': 'bend',
                                   'deformFlare': 'flare',
                                   'deformSine': 'sine',
                                   'deformSquash': 'squash',
                                   'deformTwist': 'twist',
                                   'deformWave': 'wave'}
                                   
                # Get the shape of the selected object
                shape = cmds.listRelatives(transform_list, shapes=True, noIntermediate=True)
                # Get the skinClusters and blendShapes that are connected to the shape
                skin_list = cmds.listConnections(shape, type='skinCluster')
                blendShape_list = cmds.listConnections(shape, type='blendShape')
                # Rename the selected skinClusters and blendShapes
                for skin in skin_list:
                    cmds.rename(skin, '{}_{}_skin'.format(skin.split('_')[0],
                                                          skin.split('_')[1]))
                for bs in blendShape_list:
                    cmds.rename(bs, '{}_{}_bs'.format(bs.split('_')[0],
                                                        bs.split('_')[1]))


                history_nodes = cmds.listHistory(shape, pdo=True)
                for history_node in history_nodes:
                    if 'geometryFilter' in cmds.nodeType(history_node, i=True, d=False):
                        type = cmds.nodeType(history_node)
                        if type == 'nonLinear':
                            deform_shape = cmds.listConnections('{}.deformerData'.format(history_node), s=True, d=False, sh=True)
                            if not deform_shape:
                                continue
                            nonLinear_type = cmds.nodeType(deform_shape[0])
                            if nonLinear_type not in nonLinear_types:
                                continue
                            type = nonLinear_types[nonLinear_type]
                        nodes_name = '{}_{}_{}'.format(node.split('_')[0], node.split('_')[1], type)
                        cmds.rename(history_node, nodes_name)
                    else:
                        type = cmds.nodeType(history_node, i=True, d=False)[0]
                        nodes_name = (node.split('_')[0], node.split('_')[1], type)

def rename_bind_poses():
    bind_pose_list = cmds.ls(type='dagPose')
    if bind_pose_list:
        for bind_pose in bind_pose_list:
            skin_connections = cmds.listConnections(bind_pose, type='skinCluster')
            if skin_connections:
                skin_node = skin_connections[0]
                bind_pose_name = '{}_bp'.format(skin_node)
                cmds.rename(bind_pose, bind_pose_name)
    else:
        pass

def rename_unit_conversion():
    uc_list = cmds.ls(type='unitConversion')
    if uc_list:
        for uc in uc_list:
            uc_connection = cmds.listConnections('{}.output'.format(uc), plugs=True)
            uc_output = uc_connection[0]
            if len(uc_output.split('.')[0].split('_')) == 2:
                descriptor, side, usage = uc_output.split('.')[0].split('_')
                cmds.rename(uc, '{}{}_{}_{}_bp'.format(descriptor, uc_output.split('.')[1].capitalize(), side, usage))
            else:
                cmds.rename(uc, '{}{}_bp'.format(uc_output.split('.')[0], uc_output.split('.')[1].capitalize()))
    else:
        pass
