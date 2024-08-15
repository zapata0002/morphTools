import maya.cmds as cmds
curve1 = []
curve1.append(cmds.curve( p =[(-0.5, 0.0, 0.0), (-0.5, 0.0, 1.0), (0.5, 0.0, 1.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), (-1.0, 0.0, 0.0), (-0.5, 0.0, 0.0)],per = False, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7]))
fp = cmds.listRelatives(curve1[0], f=True)[0]
path = fp.split("|")[1]
cmds.select(path)