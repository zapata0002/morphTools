import maya.cmds as cmds

class Connexion:
	def __init__(self, driver=None, driven=None, connexion_type='local'):
		self.driver = driver
		self.driven = driven
		self.connexion_type = connexion_type

		if connexion_type == 'local' or 'Local':
			self.local_connexion(translation=True, rotate=True, scale=True, visibility=False)
		elif connexion_type == 'matrix' or 'Matrix':
			self.matrix_connexion(translation=True, rotate=True, scale=True)
		elif connexion_type == 'constraint' or 'Constraint':
			self.constraint_connexion(parent=True, scale=True, maintainOffset=True, weight=1)
		else:
			raise Exception('That connexion type is invalid (choose between "local", "matrix" or "constraint")')

	def local_connexion(self, translation=False, rotate=False, scale=False, visibility=False):
		if len([self.driven] + [self.driver]) < 2:
			cmds.warning('Select driver and driven nodes')
		if len([self.driven] + [self.driver]) > 2:
			cmds.warning('Select driver and driven nodes')
		if len([self.driven] + [self.driver]) == 2:
			if translation:
				for axis in 'XYZ':
					cmds.connectAttr('{}.translate.translate{}'.format(self.driver, axis), '{}.translate.translate{}'.format(self.driven, axis), force=True)
			if rotate:
				for axis in 'XYZ':
					cmds.connectAttr('{}.rotate.rotate{}'.format(self.driver, axis), '{}.rotate.rotate{}'.format(self.driven, axis), force=True)
			if scale:
				for axis in 'XYZ':
					cmds.connectAttr('{}.scale.scale{}'.format(self.driver, axis), '{}.scale.scale{}'.format(self.driven, axis), force=True)
			if visibility:
				cmds.connectAttr('{}.v'.format(self.driver), '{}.v'.format(self.driven), force=True)

	def matrix_connexion(self, translation=False, rotate=False, scale=False):
		if len([self.driven] + [self.driver]) < 2:
			cmds.warning('Select driver and driven nodes')
		if len([self.driven] + [self.driver]) > 2:
			cmds.warning('Select driver and driven nodes')
		if len([self.driven] + [self.driver]) == 2:
			if len(self.driven.split('_')) == 3:
				descriptor, side, usage = self.driven.split('_')
				mult_matrix_node='{}{}_{}_multmat'.format(descriptor, usage.capitalize(), side)
				decompose_matrix_node='{}{}_{}_decmat'.format(descriptor, usage.capitalize(), side)
				mult_matrix_node = cmds.createNode('multMatrix', name=mult_matrix_node)
				decompose_matrix_node = cmds.createNode('decomposeMatrix', name=decompose_matrix_node)
			else:
				mult_matrix_node = '{}_multmat'.format(self.driven)
				decompose_matrix_node = '{}_decmat'.format(self.driven)
				mult_matrix_node = cmds.createNode('multMatrix', name=mult_matrix_node)
				decompose_matrix_node = cmds.createNode('decomposeMatrix', name=decompose_matrix_node)
			#Build connections between nodes
			cmds.connectAttr('{}.worldMatrix[0]'.format(self.driver),'{}.matrixIn[0]'.format(mult_matrix_node))
			cmds.connectAttr('{}.parentInverseMatrix[0]'.format(self.driver),'{}.matrixIn[1]'.format(mult_matrix_node))
			cmds.connectAttr('{}.matrixSum'.format(mult_matrix_node),'{}.inputMatrix'.format(decompose_matrix_node))
			if translation:
				cmds.connectAttr('{}.outputTranslate'.format(decompose_matrix_node),'{}.translate'.format(self.driven))
			if rotate:
				cmds.connectAttr('{}.outputRotate'.format(decompose_matrix_node),'{}.rotate'.format(self.driven))
			if scale:
				cmds.connectAttr('{}.outputScale'.format(decompose_matrix_node),'{}.scale'.format(self.driven))

	def constraint_connexion(self, parent=False, point=False, orient=False, scale=False,
							 maintainOffset=False, weight=1, skipTranslation=None,
							 skipRotate=None, skipScale=None, remove=False):
		if len([self.driven] + [self.driver]) < 2:
			cmds.warning('Select driver and driven nodes')
		if len([self.driven] + [self.driver]) > 2:
			cmds.warning('Select driver and driven nodes')
		if len([self.driven] + [self.driver]) == 2:
			if parent:
				pacns = cmds.parentConstraint(self.driver, self.driven, maintainOffset=maintainOffset, weight=weight)[0]
				if skipTranslation:
					if skipRotate:
						cmds.parentConstraint(pacns, edit=True, skipTranslation=skipTranslation, skipRotate=skipRotate)
				else:
					if skipRotate:
						cmds.parentConstraint(pacns, edit=True, skipRotate=skipRotate)
				if remove:
					cmds.parentConstraint(self.driver, self.driven, edit=True, remove=True)
			if point:
				pocns = cmds.pointConstraint(self.driver, self.driven, maintainOffset=maintainOffset, weight=weight)[0]
				if skipTranslation:
					cmds.pointConstraint(pocns, edit=True, skip=skipTranslation)
				if remove:
					cmds.pointConstraint(self.driver, self.driven, edit=True, remove=True)
			if orient:
				orcns = cmds.orientConstraint(self.driver, self.driven, maintainOffset=maintainOffset, weight=weight)[0]
				if skipRotate:
					cmds.orientConstraint(orcns, edit=True, skip=skipRotate)
				if remove:
					cmds.orientConstraint(self.driver, self.driven, edit=True, remove=True)
			if scale:
				sccns = cmds.scaleConstraint(self.driver, self.driven, maintainOffset=maintainOffset, weight=weight)[0]
				if skipScale:
					cmds.scaleConstraint(sccns, edit=True, skip=skipScale)
				if remove:
					cmds.scaleConstraint(self.driver, self.driven, edit=True, remove=True)
