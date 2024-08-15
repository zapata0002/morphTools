
#Create Attribute 
sel_list = cmds.ls(sl=True)
for ctl in sel_list:
	cmds.select(ctl)
	cmds.addAttr(ln='SEP01', nn=' ', at='enum', en='Attributes')
	cmds.setAttr('{}.SEP01'.format(ctl), e=True, k=False, cb=True)


#Create reverse control
ctl_list = cmds.ls(sl=True)
for ctl in ctl_list:
	reverse_name = '{}{}_{}_reverse'.format(ctl.split('_')[0],ctl.split('_')[2].capitalize(), ctl.split('_')[1])
	reverse_node = cmds.createNode('transform', n=reverse_name)
	cmds.matchTransform(reverse_node, ctl)
	father_node = cmds.listRelatives(ctl, p=True)
	cmds.parent(reverse_node, father_node)
	cmds.parent(ctl, reverse_node)
	
	multiply_name = '{}{}Reverse_{}_mult'.format(ctl.split('_')[0],
												ctl.split('_')[2].capitalize(),
												ctl.split('_')[1])
	multiply_node = cmds.createNode('multiplyDivide', n=multiply_name)
	cmds.setAttr('{}.input2X'.format(multiply_node), -1)
	cmds.setAttr('{}.input2Y'.format(multiply_node), -1)
	cmds.setAttr('{}.input2Z'.format(multiply_node), -1)
	cmds.connectAttr('{}.translate'.format(ctl),'{}.input1'.format(multiply_node), f=True)
	cmds.connectAttr('{}.output'.format(multiply_node),'{}.translate'.format(reverse_node), f=True)

#Build connection between control and joint
driver = cmds.ls(sl=True)[0]
driven = cmds.ls(sl=True)[1]

for attr in 'trs':
	for axis in 'xyz':
		cmds.connectAttr('{}.{}{}'.format(driver, attr, axis),
						 '{}.{}{}'.format(driven, attr, axis), f=True )


#Add key to sdk
animCurves = cmds.ls(sl=True)

def add_keys(node, values):
	for each in values:
		f, v = each
		cmds.setKeyframe(node, f=f, v=v)

for each in animCurves:
	last_index = cmds.keyframe(each, q=True, iv=True)
	if last_index:
		i = int(last_index[-1]) + 1
	else:
		i = 0
	values = [(i, 0.0)]
	add_keys(each, values)

#Rebuild target blendshape
blendshape_list = cmds.ls(sl=True, type='blendShape')

for bs in blendshape_list:
	cmds.setAttr('{}.deformationOrder'.format(bs), False)


