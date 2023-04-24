import maya.cmds as cmds

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
    for shape in cmds.listRelatives(crv, shapes=True):
        crv_data[crv] = dict()
        crv_cv = cmds.ls('{}.cv[*]'.format(shape), flatten=True)
        crv_degree = cmds.getAttr('{}.degree'.format(shape))
        crv_per = cmds.getAttr('{}.form'.format(shape))
        for cv in crv_cv:
            cv_pos = cmds.xform(cv, query=True, translation=True, worldSpace=True)
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


def build_curve_from_transforms_list(name=None, transform_list=None, degree=3, construction_history=False, parent_curve_on_root=False):
    for transform in transform_list:
        if not cmds.objExists(transform):
            raise Exception('given object does not exists in the scene: "{}"'.format(transform))
        if cmds.objectType(transform) not in ['transform', 'joint']:
            raise Exception('given object " {} " is not a transform'.format(transform))
    if len(transform_list) < degree+1:
        raise Exception('given transform_list need to have {} objects'.format(self.degree+1))
    # Build curve from transforms
    if len(transform_list[0].split('_')) == 2:
        curve_name = transform_list[0].replace('_loc', '_crv')
    else:
        curve_name = name
    point_list = []
    for transform in transform_list[0]:
        point_list.append(cmds.xform(transform, worldSpace=True, query=True, translation=True))
    curve_node = cmds.curve(degree=degree,
                            point=point_list,
                            name=curve_name)
    # Rename curve shape
    curve_shape = cmds.listRelatives(curve_node, shapes=True)[0]
    curve_shape = cmds.rename(curve_shape, '{}Shape'.format(curve_node))
    # Construction history options
    if construction_history:
        for cv_index, transform in enumerate(transform_list):
            descriptor, side, usage = transform.split('_')
            point_matrix_mult = '{}{}{}_{}_pmm'.format(descriptor,
                                                       usage[0].upper(),
                                                       usage[1:],
                                                       side)
            matrix_connection_plug = '{}.worldMatrix[0]'.format(transform)
            if cmds.objExists(point_matrix_mult):
                mult_matrix = cmds.createNode('multMatrix',
                                              name='{}{}{}_{}_multmat'.format(descriptor,
                                                                              usage[0].upper(),
                                                                              usage[1:],
                                                                              side))
                cmds.connectAttr('{}.worldMatrix[0]'.format(transform),
                                 '{}.matrixIn[0]'.format(mult_matrix))
                cmds.connectAttr('{}.worldInverseMatrix[0]'.format(transform_list[0]),
                                 '{}.matrixIn[1]'.format(mult_matrix))
                matrix_connection_plug = '{}.matrixSum'.format(mult_matrix)
            if not cmds.objExists(point_matrix_mult):
                point_matrix_mult = cmds.createNode('pointMatrixMult',
                                                    name=point_matrix_mult)
                cmds.connectAttr(matrix_connection_plug,
                                 '{}.inMatrix'.format(point_matrix_mult))

            cmds.connectAttr('{}.output'.format(point_matrix_mult),
                             '{}.controlPoints[{}]'.format(curve_shape, cv_index))
    # Parent curve on transform
    if parent_curve_on_root:
        cmds.parent(curve_node, transform_list[0])


def odd_cvs(crv):
    cv_count = cmds.getAttr(crv + '.spans') + cmds.getAttr(crv + '.degree')
    cv_list = ['{}.cv[{}]'.format(crv, i) for i in range(cv_count) if i % 2 == 1]
    return cv_list


def even_cvs(crv):
    cv_count = cmds.getAttr(crv + '.spans') + cmds.getAttr(crv + '.degree')
    cv_list = ['{}.cv[{}]'.format(crv, i) for i in range(cv_count) if i % 2 == 0]
    return cv_list


def stretch_curve(crv, joint_list, axis):
    crv_shape = cmds.listRelatives(crv, shapes=True)[0]
    cinfo_node = cmds.createNode('curveInfo', name='{}Lenght_{}_cinfo'.format(crv.split('_')[0], crv.split('_')[1] ))
    norm_node = cmds.createNode('multiplyDivide', name='{}Lenght_{}_norm'.format(crv.split('_')[0], crv.split('_')[1] ))
    global_norm_node = cmds.createNode('multiplyDivide', name='{}GlobalScale_{}_norm'.format(crv.split('_')[0], crv.split('_')[1] ))
    cmds.setAttr('{}.operation'.format(norm_node), 2)
    cmds.setAttr('{}.operation'.format(global_norm_node), 2)
    cmds.connectAttr('{}.worldSpace[0]'.format(crv_shape), '{}.inputCurve'.format(cinfo_node))
    cmds.connectAttr('{}.arcLength'.format(cinfo_node), '{}.input1.input1X'.format(norm_node))
    cmds.connectAttr('{}.output.outputX'.format(norm_node), '{}.input1.input1X'.format(global_norm_node))
    crv_lenght = cmds.getAttr('{}.arcLength'.format(cinfo_node))
    cmds.setAttr('{}.input2.input2X'.format(norm_node),crv_lenght)
    for jnt in joint_list:
        mult_node = cmds.createNode('multDoubleLinear', name='{}{}Lenght_{}_mult'.format(jnt.split('_')[0],jnt.split('_')[2].capitalize(), jnt.split('_')[1]))
        jnt_distance = cmds.getAttr('{}.translate.translate{}'.format(jnt, axis))
        cmds.setAttr('{}.input1'.format(mult_node), jnt_distance)
        cmds.connectAttr('{}.output.outputX'.format(global_norm_node), '{}.input2'.format(mult_node))
        cmds.connectAttr('{}.output'.format(mult_node), '{}.translate.translate{}'.format(jnt, axis))

