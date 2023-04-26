"""
Usage for nodes in maya

#Import shape_lib module
from maya_lib.libs import usage_lib
"""

# Control usages
control = 'ctr'

# Joint usages
skin_joint = 'skn'
joint = 'jnt'
nurbs_skin_joint = 'nskn'
curve_skin_joint = 'cskn'

# Guide usages
guide = 'guide'

# Nurbs usages
nurbs = 'nurbs'

# Constraint usages
parent_constraint = 'pacns'
orient_constraint = 'orcns'
point_constraint = 'pocns'
scale_constraint = 'sccns'
aim_constraint = 'aicns'
pole_vector_constraint = 'pvcns'

geometry = 'geo'
trigger = 'trg'
driver = 'driver'
bind = 'bind'

# Deformers
skin_cluster = 'skin'
blend_shape = 'bs'
corrective = 'crr'


multiply = 'mult'
divide = 'div'
add = 'add'
sub = 'sub'
maximum = 'max'
minimum = 'min'
distance = 'dist'
curve = 'crv'
locator = 'loc'
group = 'grp'
zero = 'zero'
null = 'null'
set_driven_key = 'sdk'
reference = 'ref'
uvpin = 'uvp'
curve_info = 'cinfo'
norm = 'norm'
blend_color = 'bc'
ik_handle = 'ikh'
ik_spline = 'iks'
effector = 'eff'
power = 'pow'
remap_value = 'rv'
reverse = 'rev'
clamp = 'clamp'
mult_matrix = 'multmat'
inverse_matrix = 'invmat'
decompose_matrix = 'decmat'
compose_matrix = 'cmat'
aim_matrix = 'aimmat'
blend_matrix = 'blendmat'
pick_matrix = 'pickmat'
point_matrix_mult = 'pmatmult'
quat_to_euler = 'qte'
point_on_curve_info = 'pocinfo'
nearest_point_on_curve = 'npoc'


def get_usage_capitalize(usage):
    return '{}{}'.format(usage[0].upper(), usage[1:])