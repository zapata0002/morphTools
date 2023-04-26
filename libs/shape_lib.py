# Imports
import importlib
import maya.cmds as cmds
from maya_lib.libs import curve_lib
importlib.reload(curve_lib)


'''
#Import shape_lib module
from maya_lib.libs import shape_lib

type = 'plus'
shape_lib.ShapeLib(type=type, name='{}_c_ctr'.format(type), scale=5)
'''


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
        if type == 'allDirections3D':
            self.create_allDirections3D()
        if type == 'cylinder':
            self.create_cylinder()

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

    def create_general(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(-0.6411898986754146, 0.005116290412843227, 0.1585763273843136), (-0.729070580862966, 0.0108537832275033, 0.15857640054627256),
                                                              (-0.7290705808629662, 0.0108537832275033, 0.26755882082465493), (-0.9965799198158629, 0.0108537832275033, 4.9416056954529955e-05),
                                                              (-0.7290705808629647, 0.0108537832275033, -0.26745997901773816), (-0.7290705808629647, 0.0108537832275033, -0.1584775709330155),
                                                              (-0.6411898986754135, 0.005116290412843227, -0.15847764409497467), (-0.6231527443454772, 5.739271580957505e-17, -0.23633066279488177),
                                                              (-0.5901227535837925, 5.435063668418063e-17, -0.3097203020417215), (-0.548487453177508, 5.0515999417952205e-17, -0.37859353160871184),
                                                              (-0.4988539410643126, 4.5944728037743257e-17, -0.4419460328941874), (-0.4419460328941859, 4.070347675731331e-17, -0.4988539410643142),
                                                              (-0.37859353160871007, 3.486867706526226e-17, -0.5484874531775092), (-0.30972030204171946, 2.8525416068119765e-17, -0.5901227535837935),
                                                              (-0.23633066279487955, 2.176618744762028e-17, -0.6231527443454778), (-0.1585763273843136, 0.005116290412843227, -0.6411898986754146),
                                                              (-0.1585764005462738, 0.0108537832275033, -0.7290705808629653), (-0.2675588208246562, 0.0108537832275033, -0.7290705808629653),
                                                              (-4.9416056956189584e-05, 0.0108537832275033, -0.9965799198158625), (0.26745997901773694, 0.0108537832275033, -0.7290705808629653),
                                                              (0.15847757093301426, 0.0108537832275033, -0.7290705808629653), (0.15847764409497359, 0.005116290412843227, -0.6411898986754143),
                                                              (0.23633066279488069, 5.739271580957505e-17, -0.6231527443454774), (0.30972030204172035, 5.435063668418063e-17, -0.5901227535837933),
                                                              (0.37859353160871134, 5.0515999417952205e-17, -0.5484874531775087), (0.44194603289418644, 4.5944728037743257e-17, -0.4988539410643132),
                                                              (0.4988539410643134, 4.070347675731331e-17, -0.4419460328941863), (0.5484874531775086, 3.486867706526226e-17, -0.37859353160871106),
                                                              (0.5901227535837927, 2.8525416068119765e-17, -0.3097203020417205), (0.6231527443454775, 2.176618744762028e-17, -0.23633066279488063),
                                                              (0.6411898986754135, 0.005116290412843227, -0.15857632738431438), (0.7290705808629652, 0.0108537832275033, -0.15857640054627395),
                                                              (0.7290705808629652, 0.0108537832275033, -0.26755882082465654), (0.9965799198158629, 0.0108537832275033, -4.9416056956632176e-05),
                                                              (0.7290705808629657, 0.0108537832275033, 0.2674599790177365), (0.7290705808629657, 0.0108537832275033, 0.15847757093301407),
                                                              (0.6411898986754138, 0.005116290412843227, 0.15847764409497325), (0.6231527443454778, 5.739271580957505e-17, 0.23633066279488052),
                                                              (0.590122753583793, 5.435063668418063e-17, 0.30972030204172013), (0.548487453177509, 5.0515999417952205e-17, 0.37859353160871084),
                                                              (0.49885394106431363, 4.5944728037743257e-17, 0.4419460328941861), (0.44194603289418655, 4.070347675731331e-17, 0.4988539410643131),
                                                              (0.37859353160871134, 3.486867706526226e-17, 0.5484874531775086), (0.3097203020417207, 2.8525416068119765e-17, 0.5901227535837924),
                                                              (0.2363306627948811, 2.176618744762028e-17, 0.6231527443454774), (0.15857632738431482, 0.005116290412843227, 0.641189898675414),
                                                              (0.158576400546275, 0.0108537832275033, 0.7290705808629652), (0.2675588208246571, 0.0108537832275033, 0.7290705808629652),
                                                              (4.941605695763936e-05, 0.0108537832275033, 0.9965799198158625), (-0.2674599790177359, 0.0108537832275033, 0.729070580862966),
                                                              (-0.15847757093301335, 0.0108537832275033, 0.7290705808629658), (-0.15847764409497267, 0.005116290412843227, 0.6411898986754146),
                                                              (-0.23633066279487983, 5.739271580957505e-17, 0.6231527443454778), (-0.3097203020417196, 5.435063668418063e-17, 0.5901227535837935),
                                                              (-0.3785935316087102, 5.0515999417952205e-17, 0.5484874531775092), (-0.441946032894186, 4.5944728037743257e-17, 0.4988539410643141),
                                                              (-0.4988539410643128, 4.070347675731331e-17, 0.4419460328941874), (-0.548487453177508, 3.486867706526226e-17, 0.37859353160871184),
                                                              (-0.5901227535837925, 2.8525416068119765e-17, 0.3097203020417212), (-0.6231527443454772, 2.176618744762028e-17, 0.23633066279488177),
                                                              (-0.6411898986754146, 0.005116290412843227, 0.1585763273843136)])

        shape = cmds.listRelatives(self.control, shapes=True)[0]
        cmds.rename(shape, '{}Shape'.format(self.control))
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control))
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control)
        return self.control[0]

    def create_eye(self):
        self.control = cmds.circle(name=self.name, normal=(0, 1, 0), radius=0.6)
        shape = cmds.listRelatives(self.control, shapes=True)[0]
        shape = cmds.rename(shape, '{}Shape'.format(self.control[0]))
        control_1 = cmds.circle(name='{}1'.format(self.name), normal=(0, 1, 0), radius=1)
        shape_1 = cmds.listRelatives(control_1, shapes=True)[0]
        shape_1 = cmds.rename(shape_1, '{}1'.format(shape))
        cmds.scale(1.5, 1, 0, curve_lib.even_cvs(control_1[0])[:-2], relative=True)
        cmds.parent(shape_1, self.control[0], shape=True, relative=True)
        cmds.scale(self.scale, self.scale, self.scale, '{}.cv[*]'.format(self.control[0]))
        cmds.delete(control_1)
        cmds.delete(self.control, constructionHistory=True)
        cmds.select(self.control[0])
        return self.control[0]

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

    def create_allDirections3D(self):
        self.control = cmds.curve(name=self.name, degree=1, point=[(0.7499114722428128, 0.07499114722428132, -0.24997049074760422),
                                                              (0.7499114722428128, -0.07499114722428132, -0.24997049074760422),
                                                              (0.9998819629904169, 0.0, -0.24997049074760422),
                                                              (0.7499114722428128, 0.07499114722428132, -0.24997049074760422),
                                                              (0.7499114722428128, 0.07499114722428132, 0.24997049074760422),
                                                              (0.9998819629904169, 0.0, 0.24997049074760422),
                                                              (0.9998819629904169, 0.0, -0.24997049074760422),
                                                              (0.7499114722428128, -0.07499114722428132, -0.24997049074760422),
                                                              (0.7499114722428128, -0.07499114722428132, 0.24997049074760422),
                                                              (0.9998819629904169, 0.0, 0.24997049074760422),
                                                              (0.7499114722428128, 0.07499114722428132, 0.24997049074760422),
                                                              (0.7499114722428128, -0.07499114722428132, 0.24997049074760422)])

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


