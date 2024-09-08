# Imports
import maya.cmds as mc
from maya_lib.libs import usage_lib, attribute_lib
import importlib
importlib.reload(attribute_lib)
"""
#Import shape_lib module
from maya_lib.libs import curve_lib
import importlib
importlib.reload(curve_lib)

curve_lib.CurveLib()
curve_lib.select_odd_cvs(crv)

"""


def get_curve_data(crv):
    """
    Get curve data
    :param crv: string
    :return: crv_data
    """
    crv_data = dict()
    cvs_pos = list()
    for shape in mc.listRelatives(crv, shapes=True):
        crv_data[crv] = dict()
        crv_cv = mc.ls('{}.cv[*]'.format(shape), flatten=True)
        crv_degree = mc.getAttr('{}.degree'.format(shape))
        crv_per = mc.getAttr('{}.form'.format(shape))
        for cv in crv_cv:
            cv_pos = mc.xform(cv, query=True, translation=True, worldSpace=True)
            cvs_pos.append(cv_pos)
        crv_data[crv]['periodic'] = False
        if crv_per == 2:
            crv_knot = []
            for index in range(crv_degree):
                cvs_pos.append(cvs_pos[index])
                for i in range(len(cvs_pos) + crv_degree - 1):
                    crv_knot = i
            crv_data[crv]['periodic'] = True
            crv_data[crv]['knot'] = crv_knot
        crv_data[crv]['degree'] = crv_degree
        crv_data[crv]['point'] = cvs_pos
    return crv_data


def stretch_curve(crv, joint_list):
    crv_shape = mc.listRelatives(crv, shapes=True)[0]
    cinfo_node = mc.createNode('curveInfo', name='{}_{}_{}'.format(crv.split('_')[0], crv.split('_')[1],
                                                                     usage_lib.curve_info))
    norm_node = mc.createNode('multiplyDivide', name='{}_{}_{}'.format(crv.split('_')[0], crv.split('_')[1],
                                                                         usage_lib.norm))
    mc.setAttr('{}.operation'.format(norm_node), 2)
    mc.connectAttr('{}.worldSpace[0]'.format(crv_shape), '{}.inputCurve'.format(cinfo_node))
    mc.connectAttr('{}.arcLength'.format(cinfo_node), '{}.input1.input1X'.format(norm_node))
    crv_length = mc.getAttr('{}.arcLength'.format(cinfo_node))
    mc.setAttr('{}.input2.input2X'.format(norm_node), crv_length)
    global_norm_node = mc.createNode('multiplyDivide', name='{}GlobalScale_{}_{}'.format(crv.split('_')[0],
                                                                                           crv.split('_')[1],
                                                                                           usage_lib.norm))
    mc.setAttr('{}.operation'.format(global_norm_node), 2)
    mc.connectAttr('{}.output.outputX'.format(norm_node), '{}.input1.input1X'.format(global_norm_node))
    for jnt in joint_list:
        mult_node = mc.createNode('multDoubleLinear', name='{}{}_{}_{}'.format(jnt.split('_')[0],
                                                                                 jnt.split('_')[2].capitalize(),
                                                                                 jnt.split('_')[1],
                                                                                 usage_lib.multiply))
        jnt_distance = mc.getAttr('{}.translate.translateX'.format(jnt))
        mc.setAttr('{}.input1'.format(mult_node), jnt_distance)
        mc.connectAttr('{}.output.outputX'.format(global_norm_node), '{}.input2'.format(mult_node))
        mc.connectAttr('{}.output'.format(mult_node), '{}.translate.translateX'.format(jnt))
    return global_norm_node


def auto_squash(joint_list, module):
    """
    Auto squash system
    :param joint_list: list
    :param module: str

    :return: crv_data
    """
    # Create bc and sub nodes
    bc_node = mc.createNode('blendColors', name='{}AutoSquash_{}_{}'.format(module.split('_')[0],
                                                                              joint_list[0].split('_')[1],
                                                                              usage_lib.blend_color))
    sub_node = mc.createNode('plusMinusAverage', name='{}_{}_{}'.format(module.split('_')[0],
                                                                          joint_list[0].split('_')[1],
                                                                          usage_lib.sub))
    # Connect bc and sub
    mc.connectAttr('{}.output.outputR'.format(bc_node), '{}.input3D[0].input3Dx'.format(sub_node))
    mc.connectAttr('{}.output.outputG'.format(bc_node), '{}.input3D[0].input3Dy'.format(sub_node))
    # Set sub noden
    mc.setAttr('{}.operation'.format(sub_node), 2)
    mc.setAttr('{}.input3D[1].input3Dx'.format(sub_node), 1)
    mc.setAttr('{}.input3D[1].input3Dy'.format(sub_node), 1)
    # Create auto squash null values
    null_node = mc.createNode('transform', name='{}AutoSquashValues_{}_{}'.format(module.split('_')[0],
                                                                                    joint_list[0].split('_')[1],
                                                                                    usage_lib.null))
    # Parent to spineSystem_c_grp
    mc.parent(null_node, 'spineSystem_c_grp')
    # Lock and hide attributes
    attr_list = []
    for attr in ['translate', 'rotate', 'scale']:
        for axis in ['X', 'Y', 'Z']:
            attr_name = '{}{}'.format(attr, axis)
            attr_list.append(attr_name)
    null_helper = attribute_lib.Helper(null_node)
    null_helper.lock_and_hide_attributes(attr_list)
    for index, jnt in enumerate(joint_list):
        # Create attribute
        squash_attr = null_helper.add_float_attribute('{}'.format(jnt.split('_')[0]))
        # Create mult and sum nodes
        mult_node = mc.createNode('multiplyDivide', name='{}AutoSquash_{}_{}'.format(jnt.split('_')[0],
                                                                                       jnt.split('_')[1],
                                                                                       usage_lib.multiply))
        add_node = mc.createNode('plusMinusAverage', name='{}AutoSquash_{}_{}'.format(jnt.split('_')[0],
                                                                                        jnt.split('_')[1],
                                                                                        usage_lib.add))
        # Set mult and sum nodes
        mc.setAttr('{}.operation'.format(mult_node), 1)
        mc.setAttr('{}.input2X'.format(mult_node), 1)
        mc.setAttr('{}.input2Y'.format(mult_node), 1)
        mc.setAttr('{}.operation'.format(add_node), 1)
        mc.setAttr('{}.input3D[1].input3Dx'.format(add_node), 1)
        mc.setAttr('{}.input3D[1].input3Dy'.format(add_node), 1)
        # Set squash values
        joint_number = len(joint_list)
        if index == 0 or index == joint_number - 1:
            squash_value = 1
        else:
            squash_value = (index / ((joint_number - 1) / 2)) / 2
            if squash_value > 1:
                squash_value = (2 - squash_value)
        mc.setAttr('{}.{}'.format(null_node, squash_attr), squash_value)
        mc.connectAttr('{}.{}'.format(null_node, squash_attr), '{}.input2.input2X'.format(mult_node))
        mc.connectAttr('{}.{}'.format(null_node, squash_attr), '{}.input2.input2Y'.format(mult_node))
        # Connect nodes
        mc.connectAttr('{}.output3D.output3Dx'.format(sub_node), '{}.input1X'.format(mult_node))
        mc.connectAttr('{}.output3D.output3Dy'.format(sub_node), '{}.input1Y'.format(mult_node))
        mc.connectAttr('{}.output.outputX'.format(mult_node), '{}.input3D[0].input3Dx'.format(add_node))
        mc.connectAttr('{}.output.outputY'.format(mult_node), '{}.input3D[0].input3Dy'.format(add_node))
        mc.connectAttr('{}.output3D.output3Dx'.format(add_node), '{}.scale.scaleY'.format(jnt))
        mc.connectAttr('{}.output3D.output3Dx'.format(add_node), '{}.scale.scaleZ'.format(jnt))
    return bc_node
'''
import math

num_list = []
num_elements = 11
middle_joint = num_elements / 2
for index in range(num_elements):
    if index == 0 or index == num_elements-1:
        value = 1
        print(index, value)
    elif num_elements % 2 == 0:
        print('par')
        if index == middle_joint or index == math.floor(middle_joint-1):
            value = 0.5
            print(index, value)
        elif index == math.floor(middle_joint):
            value = 0.55
            print(index, value)
        elif index > 0 and index < middle_joint:
            value = .25
            print(index, value)
        elif index < num_elements and index > middle_joint:
            value = .75
            print(index, value)
    elif num_elements % 2 == 1:
        print('impar')
        if index == math.floor(middle_joint):
            value = 0.5
            print(index, value)
        elif index > 0 and index < middle_joint:
            value = 0.25
            print(index, value)
        elif index < num_elements and index > middle_joint:
            value = 0.75
            print(index, value)


'''


def build_curve_from_transforms_list(name=None, transform_list=None, degree=3, construction_history=False,
                                     parent_curve_on_root=False):
    for transform in transform_list:
        if not mc.objExists(transform):
            raise Exception('given object does not exists in the scene: "{}"'.format(transform))
        if mc.objectType(transform) not in ['transform', 'joint']:
            raise Exception('given object " {} " is not a transform'.format(transform))
    if len(transform_list) < degree+1:
        raise Exception('given transform_list need to have {} objects'.format(degree+1))
    # Build curve from transforms
    print(transform_list[0])
    if len(transform_list[0].split('_')) == 2:
        curve_name = transform_list[0].replace('_loc', '_crv')
        print(curve_name)
    else:
        curve_name = name
        print(curve_name)
    point_list = []
    for transform in transform_list:
        point_list.append(mc.xform(transform, worldSpace=True, query=True, translation=True))
    curve_node = mc.curve(degree=degree,
                          point=point_list,
                          name=curve_name)
    # Rename curve shape
    curve_shape = mc.listRelatives(curve_node, shapes=True)[0]
    curve_shape = mc.rename(curve_shape, '{}Shape'.format(curve_node))
    # Construction history options
    if construction_history:
        for cv_index, transform in enumerate(transform_list):
            descriptor, side, usage = transform.split('_')
            point_matrix_mult = '{}{}{}_{}_pmm'.format(descriptor,
                                                       usage[0].upper(),
                                                       usage[1:],
                                                       side)
            matrix_connection_plug = '{}.worldMatrix[0]'.format(transform)
            if mc.objExists(point_matrix_mult):
                mult_matrix = mc.createNode('multMatrix',
                                              name='{}{}{}_{}_multmat'.format(descriptor,
                                                                              usage[0].upper(),
                                                                              usage[1:],
                                                                              side))
                mc.connectAttr('{}.worldMatrix[0]'.format(transform),
                                 '{}.matrixIn[0]'.format(mult_matrix))
                mc.connectAttr('{}.worldInverseMatrix[0]'.format(transform_list[0]),
                                 '{}.matrixIn[1]'.format(mult_matrix))
                matrix_connection_plug = '{}.matrixSum'.format(mult_matrix)
            if not mc.objExists(point_matrix_mult):
                point_matrix_mult = mc.createNode('pointMatrixMult',
                                                    name=point_matrix_mult)
                mc.connectAttr(matrix_connection_plug,
                                 '{}.inMatrix'.format(point_matrix_mult))

            mc.connectAttr('{}.output'.format(point_matrix_mult),
                             '{}.controlPoints[{}]'.format(curve_shape, cv_index))
    # Parent curve on transform
    if parent_curve_on_root:
        mc.parent(curve_node, transform_list[0])


def odd_cvs(crv):
    cv_count = mc.getAttr(crv + '.spans') + mc.getAttr(crv + '.degree')
    cv_list = ['{}.cv[{}]'.format(crv, i) for i in range(cv_count) if i % 2 == 1]
    return cv_list


def even_cvs(crv):
    cv_count = mc.getAttr(crv + '.spans') + mc.getAttr(crv + '.degree')
    cv_list = ['{}.cv[{}]'.format(crv, i) for i in range(cv_count) if i % 2 == 0]
    return cv_list
