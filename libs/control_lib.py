import maya.cmds as cmds
from maya_lib.libs import shape_lib, usage_lib, connexion_lib
import importlib
importlib.reload(usage_lib)


def build_control_from_guides(transform_selected_list, shape_type, jnt_usage, connexion_type):
	"""
	Build control
	:param transform_selected_list: str or list
	:param shape_type: str
	:param jnt_usage: str
	:param connexion_type: str
	"""

	previous_control = []
	previous_zero = []
	previous_joint = []
	previous_joint_zero = []
	if transform_selected_list:
		for transform in transform_selected_list:
			if not cmds.objExists(transform):
				raise Exception('given object does not exists in the scene: "{}"'.format(transform))
			if cmds.objectType(transform) not in ['transform', 'joint']:
				raise Exception('given object " {} " is not a transform'.format(transform))
			else:
				pass
			# Create control node
			descriptor, side, usage = transform.split('_')
			if not shape_type:
				control_node = cmds.createNode('transform', name='{}_{}_ctr'.format(descriptor, side))
			else:
				control_node = cmds.createNode('transform', name='{}_{}_ctr'.format(descriptor, side))
				aux_name = '{}Aux_{}_ctr'.format(descriptor, side)
				control_shape = control_shape.ControlShape(type=shape_type, name=aux_name, color=17, scale=5)
				aux_shapes = cmds.listRelatives(aux_name, shapes=True)
				for index, shape in enumerate(aux_shapes):
					cmds.parent(shape, control_node, relative=True, shape=True)
					if index == 0:
						cmds.rename(shape, '{}Shape'.format(control_node))
					else:
						cmds.rename(shape, '{}Shape{}'.format(control_node, index))
				cmds.delete(aux_name)
			usage = control_node.split('_')[2]
			# Create zero node
			control_zero = cmds.createNode('transform', name='{}{}_{}_zero'.format(descriptor, usage.capitalize(), side))
			# Add the guide position to the zero position y control node
			transform_matrix = cmds.xform(transform, query=True, matrix=True, worldSpace=True)
			cmds.xform(control_node, matrix=transform_matrix, worldSpace=True)
			cmds.xform(control_zero, matrix=transform_matrix, worldSpace=True)
			# Parent control to previous if it has a father
			cmds.parent(control_node, control_zero)
			if cmds.listRelatives(transform, parent=True):
				if previous_zero:
					cmds.parent(control_zero, previous_control)
				else:
					cmds.parent(previous_zero, control_node)
			previous_zero = control_zero
			previous_control = control_node
			# Build joint
			if jnt_usage:
				# Build skinned joint
				joint_node = cmds.createNode('joint', name=control_node.replace('ctr', jnt_usage))
				joint_zero = cmds.group(joint_node, name='{}{}_{}_zero'.format(descriptor, jnt_usage.capitalize(), side))
				# Add the control_zero position to the zero joint node
				for attr in 'trs':
					cmds.connectAttr('{}.{}'.format(control_zero, attr), '{}.{}'.format(joint_zero, attr))
				# Parent joint to previous if it has a father
				if cmds.listRelatives(transform, parent=True):
					if previous_joint_zero:
						cmds.parent(joint_zero, previous_joint)
					else:
						cmds.parent(previous_joint_zero, joint_node)
				# Build connexion between control and joint
				if connexion_type == 'constraint':
					connexion_lib.Connexion(control_node, joint_node, 'constraint')
				if connexion_type == 'local':
					connexion_lib.Connexion(control_node, joint_node, 'local')
				if connexion_type == 'matrix':
					connexion_lib.Connexion(control_node, joint_node, 'matrix')
				else:
					pass
				previous_joint_zero = joint_zero
				previous_joint = joint_node
			else:
				pass


def build_control(descriptor, side, shape):
	"""
	Build control
	:param descriptor: str
	:param side: str
	:param shape: str
	"""
	if shape:
		control_node = shape_lib.ShapeLib(type=shape, name='{}_{}_{}'.format(descriptor, side, usage_lib.control))[0]
		# Create zero node
		control_zero = cmds.createNode('transform', name='{}{}_{}_{}'.format(descriptor, usage_lib.control.capitalize(), side, usage_lib.zero))
		cmds.parent(control_node.control, control_zero)
	else:
		control_node = cmds.createNode('transform', name='{}_{}_{}'.format(descriptor, side, usage_lib.control))
	return control_node