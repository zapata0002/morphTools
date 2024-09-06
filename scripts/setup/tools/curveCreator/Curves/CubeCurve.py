import maya.cmds as cmds
curve2 = []
curve2.append(cmds.curve( p =[(-0.5692978297614414, 0.5692978297614414, -0.5692978297614414), (-0.5692978297614414, 0.5692978297614414, 0.5692978297614414), (0.5692978297614414, 0.5692978297614414, 0.5692978297614414), (0.5692978297614414, 0.5692978297614414, -0.5692978297614414), (-0.5692978297614414, 0.5692978297614414, -0.5692978297614414), (-0.5692978297614414, -0.5692978297614414, -0.5692978297614414), (0.5692978297614414, -0.5692978297614414, -0.5692978297614414), (0.5692978297614414, 0.5692978297614414, -0.5692978297614414), (0.5692978297614414, 0.5692978297614414, 0.5692978297614414), (0.5692978297614414, -0.5692978297614414, 0.5692978297614414), (0.5692978297614414, -0.5692978297614414, -0.5692978297614414), (-0.5692978297614414, -0.5692978297614414, -0.5692978297614414), (-0.5692978297614414, -0.5692978297614414, 0.5692978297614414), (0.5692978297614414, -0.5692978297614414, 0.5692978297614414), (0.5692978297614414, 0.5692978297614414, 0.5692978297614414), (-0.5692978297614414, 0.5692978297614414, 0.5692978297614414), (-0.5692978297614414, -0.5692978297614414, 0.5692978297614414)],per = False, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]))
fp = cmds.listRelatives(curve2[0], f=True)[0]
path = fp.split("|")[1]
cmds.select(path)