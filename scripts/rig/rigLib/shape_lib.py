# Imports
import importlib
import maya.cmds as cmds
from maya_lib.libs import curve_lib, side_lib
importlib.reload(curve_lib)


'''
#Import shape_lib module
from maya_lib.libs import shape_lib

type = 'plus'
shape_lib.ShapeLib(type=type, name='{}_c_ctr'.format(type), scale=5)
'''

colors_dict = {'default': 0,
               'black': 1,
               'gray': 2,
               'lightGray': 3,
               'crimson': 4,
               'darkBlue': 5,
               'blue': 6,
               'left': 6,
               side_lib.left: 6,
               'darkGreen': 7,
               'darkPurple': 8,
               'pink': 9,
               'brownLight': 10,
               'brown': 11,
               'darkOrange': 12,
               'red': 13,
               'right': 13,
               side_lib.right: 13,
               'green': 14,
               'blue2': 15,
               'white': 16,
               'yellow': 17,
               'center': 17,
               side_lib.center: 17,
               'lightBlue': 18,
               'lightGreen': 19,
               'lightPink': 20,
               'lightOrange': 21,
               'lightYellow': 22,
               'green2': 23,
               'brown2': 24,
               'pistachio': 25,
               'green3': 26,
               'green4': 27,
               'turquoise': 28,
               'blue3': 29,
               'purple': 30,
               'darkPink': 31}


def set_override_color(splines_list=None, color_key='red'):
    """
    override the spline color
    :param splines_list: list
    :param color_key: str, check valid color keys
    """
    if not splines_list:
        splines_list = cmds.ls(sl=True)

    color_value = 0
    if isinstance(color_key, int):
        if 1 <= color_key <= 31:
            color_value = color_key
        else:
            cmds.error('{} is out of range of 1 - 31'.format(color_key))
    else:
        if color_key in colors_dict.keys():
            color_value = colors_dict[color_key]
        else:
            cmds.error('{} is not a valid color, try any of these: {}'.format(color_key, list(colors_dict.keys())))

    override_value = 0 if color_value == 0 else 1
    for spl in splines_list:
        spl_shapes = cmds.listRelatives(spl, shapes=True)
        for spl_shape in spl_shapes:
            cmds.setAttr('{}.overrideEnabled'.format(spl_shape), override_value)
            cmds.setAttr('{}.overrideRGBColors'.format(spl_shape), 0)
            cmds.setAttr('{}.overrideColor'.format(spl_shape), color_value)


class ShapeLib:
    """
    :param type: ctr
    :param name: str
    :param color: int
    :param scale: int
    """
    def __init__(self, type=None, name=None, color=17, scale=1):
        self.type = type
        self.name = name
        self.color = color
        self.scale = scale
        self.control = None
        if type == 'circle':
            self.create_circle(degree=3, sections=8)
        if type == 'triangle':
            self.create_triangle()
        if type == 'square':
            self.create_square()
        if type == 'pentagon':
            self.create_circle(degree=1, sections=5)
        if type == 'hexagon':
            self.create_circle(degree=1, sections=6)
        if type == 'heptagon':
            self.create_circle(degree=1, sections=7)
        if type == 'octagon':
            self.create_circle(degree=1, sections=8)
        if type == 'nonagon':
            self.create_circle(degree=1, sections=9)
        if type == 'decagon':
            self.create_circle(degree=1, sections=10)
        if type == 'undecagon':
            self.create_circle(degree=1, sections=11)
        if type == 'dodecagon':
            self.create_circle(degree=1, sections=12)
        if type == 'plus':
            self.create_plus()
        if type == 'star':
            self.create_star()
        if type == 'arrow':
            self.create_arrow()
        if type == 'splash':
            self.create_splash()
        if type == 'general':
            self.create_general()
        if type == 'eye':
            self.create_eye()
        if type == 'box':
            self.create_box()
        if type == 'sphere':
            self.create_sphere()
        if type == 'pyramid':
            self.create_pyramid()
        if type == 'diamond':
            self.create_diamond()
        if type == 'lollipop':
            self.create_lollipop()
        if type == 'lollipop2':
            self.create_lollipop2()
        if type == 'fourPrisms':
            self.create_four_prisms()
        if type == 'cylinder':
            self.create_cylinder()
        if type == 'pelvis':
            self.create_pelvis()
        if type == 'spineFk':
            self.create_spine_fk()

    def get_control_name(self):
        if self.control:
            return self.control
        else:
            return self.name

    def create_circle(self, degree=3, sections=8):
        self.control = cmds.circle(name=self.name, degree=degree, normal=(0, 1, 0), sections=sections)[0]
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_triangle(self):
        self.control = cmds.circle(name=self.name, degree=1, sections=3, normal=(0, 1, 0))[0]
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control[0]))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_square(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1),
                                                                   (-1, 0, -1)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_plus(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-0.33, 0.0, -1.0), (-0.33, 0.0, -0.33),
                                                                   (-1.0, 0.0, -0.33), (-1.0, 0.0, 0.33),
                                                                   (-0.33, 0.0, 0.33), (-0.33, 0.0, 1.0),
                                                                   (0.33, 0.0, 1.0), (0.33, 0.0, 0.33),
                                                                   (1.0, 0.0, 0.33), (1.0, 0.0, -0.33),
                                                                   (0.33, 0.0, -0.33), (0.33, 0.0, -1.0),
                                                                   (-0.33, 0.0, -1.0)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_star(self):
        self.control = cmds.circle(name=self.name, degree=1, sections=10, normal=(0, 1, 0))[0]
        cmds.scale(0.5, 0.5, 0.5, curve_lib.odd_cvs(self.control[0]), relative=True)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control[0]))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_arrow(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-0.5, 0.0, -1.0), (0.5, 0.0, -1.0), (0.5, 0.0, 0.0),
                                                                   (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (-1.0, 0.0, 0.0),
                                                                   (-0.5, 0.0, 0.0), (-0.5, 0.0, -1.0)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.scale(1 * self.scale, 1 * self.scale, 1 * self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_splash(self):
        self.control = cmds.circle(name=self.name, degree=3, sections=8, normal=(0, 1, 0))[0]
        cmds.scale(0.05, 0.05, 0.05, curve_lib.even_cvs(self.control[0])[:-2], relative=True)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control[0]))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_four_arrows(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-0.65, 0, 0.16), (-0.73, 0.01, 0.16),
                                                                   (-0.73, 0.01, 0.27), (-0.99, 0.01, 4.95),
                                                                   (-0.73, 0, -0.26), (-0.73, 0, -0.16),
                                                                   (-0.65, 0, -0.16), (-0.62, 5.74, -0.23),
                                                                   (-0.59, 5.44, -0.31), (-0.55, 5.05, -0.38),
                                                                   (-0.50, 4.59, -0.44), (-0.44, 4.07, -0.49),
                                                                   (-0.38, 3.48, -0.54), (-0.31, 2.85, -0.59),
                                                                   (-0.24, 2.17, -0.62), (-0.15, 0, -0.64),
                                                                   (-0.16, 0, -0.72), (-0.26, 0, -0.7),
                                                                   (-4.94, 0, -0.99), (0.26, 0.01, -0.72),
                                                                   (0.16, 0, -0.72), (0.15, 0, -0.64),
                                                                   (0.24, 5.73-17, -0.62), (0.30, 5.43, -0.59),
                                                                   (0.38, 5.05-17, -0.54), (0.44, 4.59, -0.49),
                                                                   (0.50, 4.07-17, -0.44), (0.54, 3.48, -0.37),
                                                                   (0.59, 2.85-17, -0.30), (0.62, 2.17, -0.23),
                                                                   (0.64, 0, -0.15), (0.72, 0, -0.15),
                                                                   (0.73, 0, -0.26), (0.99, 0, -4.94),
                                                                   (0.73, 0, 0.26), (0.72, 0, 0.15),
                                                                   (0.64, 0, 0.16), (0.62, 5.73, 0.2),
                                                                   (0.59, 5.44, 0.30), (0.54, 5.05, 0.37),
                                                                   (0.50, 4.6, 0.44), (0.44, 4.07, 0.49),
                                                                   (0.38, 3.49, 0.55), (0.30, 2.85-17, 0.59),
                                                                   (0.24, 2.18-17, 0.62), (0.15, 0, 0.64),
                                                                   (0.16, 0.01, 0.73), (0.26, 0, 0.72),
                                                                   (4.94, 0.01, 0.99), (-0.26, 0, 0.72),
                                                                   (-0.16, 0.01, 0.73), (-0.15, 0, 0.64),
                                                                   (-0.24, 5.74-17, 0.62), (-0.30, 5.43, 0.59),
                                                                   (-0.38, 5.05-17, 0.55), (-0.44, 4.59, 0.49),
                                                                   (-0.50, 4.07, 0.44), (-0.54, 3.48, 0.37),
                                                                   (-0.59, 2.85-17, 0.3), (-0.62, 2.17, 0.23),
                                                                   (-0.65, 0, 0.15)])

        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_eye(self):
        self.control = cmds.circle(name=self.name, normal=(0, 1, 0), radius=0.6)[0]
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control))
        control_1 = cmds.circle(name='{}1'.format(self.name), normal=(0, 1, 0), radius=1)
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        cmds.scale(1.5, 1, 0, curve_lib.even_cvs(control_1[0])[:-2], relative=True)
        cmds.parent(shape_1, self.control, shape=True, relative=True)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(control_1)
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_general(self):
        self.control = cmds.curve(name=self.name, degree=3, point=[(0.33, -0.00, 1.17), (0.56, -0.00, 1.10),
                                                                   (1.08, -0.00, 0.75), (1.29, -0.00, -0.15), 
                                                                   (0.86, -0.00, -0.97), (-0.00, -0.00, -1.29), 
                                                                   (-0.87, -0.00, -0.96), (-1.29, -0.00, -0.14), 
                                                                   (-1.07, -0.00, 0.75), (-0.55, -0.00, 1.11), 
                                                                   (-0.33, -0.00, 1.17)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        control_1 = cmds.curve(name=self.name, degree=1, point=[(-0.33, 0.00, 1.17), (-0.33, 0.00, 1.36),
                                                                (-0.57, 0.00, 1.36), (0.00, 0.00, 1.93), 
                                                                (0.57, 0.00, 1.36), (0.33, 0.00, 1.36), 
                                                                (0.33, 0.00, 1.17)])
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}Shape1'.format(self.control))
        cmds.parent(shape_1, self.control, shape=True, relative=True)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(control_1)
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_pelvis(self):
        self.control = cmds.circle(name=self.name, degree=3, normal=(0, 1, 0), sections=8)[0]
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.move(0, -0.6, 0, '{}.cv[1]'.format(self.control), relative=True)
        cmds.move(0, -0.6, 0, '{}.cv[5]'.format(self.control), relative=True)
        cmds.scale(1 * self.scale, 1 * self.scale, 1 * self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control

    def create_box(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1),
                                                              (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1),
                                                              (1, -1, -1),
                                                              (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1),
                                                              (1, -1, 1),
                                                              (1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, -1, -1),
                                                              (-1, -1, 1)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(shape))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_spine_fk(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-1, 0.11, -0.99), (-1, -0.11, -0.99),
                                                                   (1, -0.11, -0.99), (1, 0.11, -0.99),
                                                                   (-1, 0.11, -0.99), (-1, 0.11, 0.99),
                                                                   (1, 0.11, 0.99), (1, 0.11, -0.99),
                                                                   (1, -0.11, -0.99), (1, -0.11, 0.99),
                                                                   (1, 0.11, 0.99), (-1, 0.11, 0.99),
                                                                   (-1, -0.11, 0.99), (1, -0.11, 0.99),
                                                                   (1, -0.11, 0.99), (1, -0.11, 0.99),
                                                                   (1, -0.11, -0.99), (-1, -0.11, -0.99),
                                                                   (-1, -0.11, 0.99)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(shape))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_sphere(self):
        self.control = cmds.circle(name=self.name, normal=(0, 1, 0), constructionHistory=False)
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control[0]))
        control_1 = cmds.circle(name='{}1'.format(self.name), normal=(0, 0, 0), constructionHistory=False)
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        control_2 = cmds.circle(name='{}2'.format(self.name), normal=(1, 0, 0), constructionHistory=False)
        shape_2 = cmds.listRelatives(control_2, shapes=True)[0]
        shape_2 = cmds.rename(shape_2, '{}2'.format(shape))
        cmds.parent(shape_1, shape_2, self.control[0], shape=True, relative=True)
        cmds.delete(control_1, control_2)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control[0])
        return self.control[0]

    def create_pyramid(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-1, 0, 0), (0, 2, 0), (0, 0, 1), (-1, 0, 0), (0, 0, -1),
                                                           (0, 2, 0), (0, 0, 1), (1, 0, 0),(0, 2, 0), (0, 0, -1),
                                                           (1, 0, 0)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(shape))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_diamond(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(0, 1.5, 0), (-1, 0, 1), (-1, 0, -1), (0, 1.5, 0), (1, 0, -1), (-1, 0, -1),
                                                            (0, -1.5, 0), (1, 0, -1), (1, 0, 1), (0, -1.5, 0), (-1, 0, 1), (1, 0, 1),
                                                            (0, 1.5, 0)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(shape))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_lollipop(self):
        self.control = cmds.circle(name=self.name, normal=(0, 1, 0), radius=0.5)
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control[0]))
        control_1 = cmds.circle(name='{}1'.format(self.name), normal=(1, 0, 0), radius=0.5)
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        control_2 = cmds.circle(name='{}2'.format(self.name), normal=(0, 0, 1), radius=0.5)
        shape_2 = cmds.listRelatives(control_2, shapes=True)[0]
        shape_2 = cmds.rename(shape_2, '{}2'.format(shape))
        control_3 = cmds.curve(name='{}3'.format(self.name), degree=1, point=[(0, 0, 0), (0, 2, 0)])
        shape_3 = cmds.listRelatives(control_3, shapes=True)[0]
        shape_3 = cmds.rename(shape_3, '{}3'.format(shape))
        cmds.parent(shape_1, shape_2, self.control[0], shape=True, relative=True)
        cmds.move(0, 2, 0, '{}.cv[:]'.format(self.control[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        cmds.parent(shape_3, self.control[0], shape=True, relative=True)
        cmds.delete(control_1, control_2, control_3)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control[0])
        return self.control[0]

    def create_lollipop2(self):
        self.control = cmds.circle(name=self.name, normal=(0, 1, 0), radius=0.5)
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control[0]))
        cmds.move(0, 2, 0, '{}.cv[:]'.format(self.control[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        control_1 = cmds.circle(name='{}1'.format(self.name), normal=(1, 0, 0), radius=0.5)
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        cmds.move(0, 2, 0, '{}.cv[:]'.format(control_1[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        control_2 = cmds.circle(name='{}2'.format(self.name), normal=(0, 0, 1), radius=0.5)
        shape_2 = cmds.listRelatives(control_2, shapes=True)[0]
        shape_2 = cmds.rename(shape_2, '{}2'.format(shape))
        cmds.move(0, 2, 0, '{}.cv[:]'.format(control_2[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        control_3 = cmds.circle(name=self.name, normal=(0, 1, 0), radius=0.5)
        shape_3 = cmds.listRelatives(control_3, shapes=True)[0]
        shape_3 = cmds.rename(shape_3, '{}3'.format(shape))
        cmds.move(0, -2, 0, '{}.cv[:]'.format(control_3[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        control_4 = cmds.circle(name='{}4'.format(self.name), normal=(1, 0, 0), radius=0.5)
        shape_4 = cmds.listRelatives(control_4, shapes=True)[0]
        shape_4 = cmds.rename(shape_4, '{}4'.format(shape))
        cmds.move(0, -2, 0, '{}.cv[:]'.format(control_4[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        control_5 = cmds.circle(name='{}5'.format(self.name), normal=(0, 0, 1), radius=0.5)
        shape_5 = cmds.listRelatives(control_5, shapes=True)[0]
        shape_5 = cmds.rename(shape_5, '{}5'.format(shape))
        cmds.move(0, -2, 0, '{}.cv[:]'.format(control_5[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        cmds.parent(shape_1, shape_2, shape_3, shape_4, shape_5,self.control[0], shape=True, relative=True)
        control_6 = cmds.curve(name='{}6'.format(self.name), degree=1, point=[(0, -2, 0), (0, 2, 0)])
        shape_6 = cmds.listRelatives(control_6, shapes=True)[0]
        shape_6 = cmds.rename(shape_6, '{}6'.format(shape))
        cmds.parent(shape_6, self.control[0], shape=True, relative=True)
        cmds.delete(control_1, control_2, control_3, control_4, control_5, control_6)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control[0])
        return self.control[0]

    def create_four_prisms(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(0.25, 0.072, 0.75), (0.25, -0.07, 0.75),
                                                                   (0.25, 0.0, 1), (0.25, 0.07, 0.75),
                                                                   (-0.25, 0.07, 0.75), (-0.25, 0.0, 1),
                                                                   (0.25, 0.0, 1), (0.25, -0.07, 0.75),
                                                                   (-0.25, -0.07, 0.75), (-0.25, 0.0, 1),
                                                                   (-0.25, 0.07, 0.75), (-0.25, -0.07, 0.75)])
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control))
        control_1 = cmds.duplicate(self.control)[0]
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        cmds.rotate(0, 90, 0, '{}.cv[:]'.format(control_1), objectSpace=True, relative=True, worldSpace=True)
        control_2 = cmds.duplicate(control_1)[0]
        shape_2 = cmds.listRelatives(control_2, shapes=True)[0]
        shape_2 = cmds.rename(shape_2, '{}2'.format(shape))
        cmds.rotate(0, 90, 0, '{}.cv[:]'.format(control_2), objectSpace=True, relative=True, worldSpace=True)
        control_3 = cmds.duplicate(control_2)[0]
        shape_3 = cmds.listRelatives(control_3, shapes=True)[0]
        shape_3 = cmds.rename(shape_3, '{}3'.format(shape))
        cmds.rotate(0, 90, 0, '{}.cv[:]'.format(control_3), objectSpace=True, relative=True, worldSpace=True)
        cmds.parent(shape_1, shape_2, shape_3, self.control, shape=True, relative=True)
        cmds.delete(control_1, control_2, control_3)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_cylinder(self):
        self.control = cmds.circle(name=self.name, normal=(0, 1, 0))
        shape = cmds.listRelatives(self.control[0], shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control[0]))
        cmds.move(0, 2, 0, '{}.cv[:]'.format(self.control[0]), objectSpace=True, relative=True, worldSpaceDistance=True)
        control_1 = cmds.circle(name='{}1'.format(self.control[0]), normal=(0, 1, 0))
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        control_2 = cmds.curve(name='{}2'.format(self.control[0]), degree=1, point=[(1, 0, 0), (1, 2, 0)])
        shape_2 = cmds.listRelatives(control_2, shapes=True)[0]
        shape_2 = cmds.rename(shape_2, '{}2'.format(shape))
        control_3 = cmds.curve(name='{}3'.format(self.control[0]), degree=1, point=[(-1, 0, 0), (-1, 2, 0)])
        shape_3 = cmds.listRelatives(control_3, shapes=True)[0]
        shape_3 = cmds.rename(shape_3, '{}3'.format(shape))
        control_4 = cmds.curve(name='{}4'.format(self.control[0]), degree=1, point=[(0, 0, -1), (0, 2, -1)])
        shape_4 = cmds.listRelatives(control_4, shapes=True)[0]
        shape_4 = cmds.rename(shape_4, '{}4'.format(shape))
        control_5 = cmds.curve(name='{}5'.format(self.control[0]), degree=1, point=[(0, 0, 1), (0, 2, 1)])
        shape_5 = cmds.listRelatives(control_5, shapes=True)[0]
        shape_5 = cmds.rename(shape_5, '{}5'.format(shape))
        cmds.parent(shape_1, shape_2, shape_3, shape_4, shape_5, self.control[0], shape=True, relative=True)
        cmds.delete(control_1, control_2, control_3, control_4, control_5)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        cmds.delete(self.control[0], constructionHistory=True)
        cmds.select(self.control[0])
        return self.control[0]


