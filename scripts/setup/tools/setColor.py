import maya.cmds as cmds


def setColor(*args):
    sel = cmds.ls(sl=True)
    if sel:
        v = cmds.colorIndexSliderGrp(color_slider, q=True, v=True)
        for obj in sel:
            shapes = cmds.listRelatives(obj, ni=True, s=True, f=True)
            if not shapes:
                continue
            for shp in shapes:
                cmds.setAttr('{}.overrideEnabled'.format(shp), True)
                cmds.setAttr('{}.overrideRGBColors'.format(shp), False)
                cmds.setAttr('{}.overrideColor'.format(shp), v-1)
    
    
def closeWindow(*args):
    if cmds.window(win, q=True, exists=True):
        cmds.deleteUI(win)
           
win = cmds.window(t='Set Color Index')
cmds.columnLayout(adjustableColumn=True)
color_slider = cmds.colorIndexSliderGrp( label='Color', min=1, max=32, value=1)
cmds.rowLayout(nc=2)
ok_button = cmds.button( label='OK', command=setColor )
cancel_button = cmds.button( label='Cancel', command=closeWindow )
cmds.showWindow(win)