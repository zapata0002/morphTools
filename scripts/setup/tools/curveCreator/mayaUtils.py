from maya import cmds, mel
import os, stat, sys, traceback, warnings, platform
from functools import wraps


def getPluginSuffix():
    """ get the current plugin suffix based on the os that we are running

    :return: suffix for plugin files specific to a particular os
    :rtype: string
    """
    pluginSuffix = ".mll"
    if platform.system() == "Darwin":
        pluginSuffix = ".bundle"
    if platform.system() == "Linux":
        pluginSuffix = ".bundle"
    return pluginSuffix


MAYAVERSION = int(str(cmds.about(apiVersion=True))[:-2])
if MAYAVERSION > 2016:
    cmds.loadPlugin("Type{}".format(getPluginSuffix()), qt=1)

_DEBUG = False
INDEXCOLORS = [[0.38, 0.38, 0.38], [0.0, 0.0, 0.0], [0.75, 0.75, 0.75],
               [0.5, 0.5, 0.5], [0.8, 0.0, 0.2], [0.0, 0.0, 0.4],
               [0.0, 0.0, 1.0], [0.0, 0.3, 0.0], [0.2, 0.0, 0.2],
               [0.8, 0.0, 0.8], [0.6, 0.3, 0.2], [0.25, 0.13, 0.13],
               [0.7, 0.2, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
               [0.0, 0.3, 0.6], [1.0, 1.0, 1.0], [1.0, 1.0, 0.0],
               [0.0, 1.0, 1.0], [0.0, 1.0, 0.8], [1.0, 0.7, 0.7],
               [0.9, 0.7, 0.7], [1.0, 1.0, 0.4], [0.0, 0.7, 0.4],
               [0.6, 0.4, 0.2], [0.63, 0.63, 0.1], [0.4, 0.6, 0.2],
               [0.2, 0.63, 0.35], [0.18, 0.63, 0.6], [0.18, 0.4, 0.63],
               [0.43, 0.18, 0.63], [0.63, 0.18, 0.4]]


def getSelection():
    return cmds.ls(sl=1, fl=1)


def hideUnselected(inBool):
    if inBool:
        mel.eval("HideUnselectedObjects;")
        return
    mel.eval("ShowLastHidden;")


def dec_undo(func):
    @wraps(func)
    def _undo_func(*args, **kwargs):
        try:
            cmds.undoInfo(ock=True)
            return func(*args, **kwargs)
        except Exception as e:
            if _DEBUG:
                print(e)
                print(e.__class__)
                print(sys.exc_info())
                warnings.warn(traceback.format_exc())
            else:
                if "Failed to create the text with the specified font" in traceback.format_exc():
                    cmds.warning("Maya does not support creation of (some of) the characters for this font")
                else:
                    cmds.warning(e)
        finally:
            cmds.undoInfo(cck=True)

    return _undo_func


def setToolTips(inBool):
    cmds.help(popupMode=inBool)


@dec_undo
def createTextController(inText, inFont):
    shapeList = []
    if MAYAVERSION > 2016:
        shapeList = createTypeToolWithNode("textCurve", font=inFont, style=None, text=inText)
        createdText = None
    else:
        createdText = cmds.textCurves(f=inFont, t=inText)
        allDescendants = cmds.listRelatives(createdText[0], ad=True)
        for desc in allDescendants:
            if 'curve' in desc and 'Shape' not in desc:
                cmds.parent(desc, w=True)
                shapeList.append(desc)

    for index, shape in enumerate(shapeList):
        cmds.makeIdentity(shape, apply=True, t=1, r=1, s=1, n=0)
        if index == 0:
            parentGuide = shapeList[0]
            continue
        foundShape = cmds.listRelatives(shape, s=True)[0]
        cmds.move(0, 0, 0, (shape + '.scalePivot'), (shape + '.rotatePivot'))
        cmds.parent(foundShape, parentGuide, add=True, s=True)
        cmds.delete(shape)

    if createdText:
        cmds.delete(createdText)
    cmds.xform(shapeList[0], cp=True)
    worldPosition = cmds.xform(shapeList[0], q=True, piv=True, ws=True)
    cmds.xform(shapeList[0], t=(-worldPosition[0], -worldPosition[1], -worldPosition[2]))
    cmds.makeIdentity(shapeList[0], apply=True, t=1, r=1, s=1, n=0)
    cmds.select(shapeList[0])


@dec_undo
def CombineCurveShapes():
    selection = cmds.ls(selection=True)
    for obj in selection:
        cmds.xform(obj, ws=True, piv=(0, 0, 0))

    cmds.makeIdentity(selection, apply=True, t=1, r=1, s=1, n=0)
    for index, obj in enumerate(selection):
        if index == 0:
            base = obj
            continue
        shapeNode = cmds.listRelatives(obj, shapes=True)
        cmds.parent(shapeNode, selection[0], add=True, s=True)
        cmds.delete(obj)
    cmds.select(base)


@dec_undo
def setDisplayType(Type):
    selection = cmds.ls(sl=True)
    if len(selection) == 0:
        cmds.warning("nothing selected")
    else:
        for Selected in selection:
            cmds.delete(Selected, ch=True)
            shapeNode = cmds.listRelatives(Selected, ad=True, s=True)
            for shapes in shapeNode:
                cmds.setAttr((shapes + ".overrideEnabled"), 1)
                cmds.setAttr((shapes + ".overrideDisplayType"), Type)
                if Type == 0:
                    cmds.setAttr((shapes + ".overrideEnabled"), 0)


@dec_undo
def setRgbColor(r, g, b, f):
    selection = cmds.ls(sl=True)
    if len(selection) == 0:
        cmds.warning("nothing selected")
    for select in selection:
        shapes = cmds.listRelatives(select, ad=True, s=True, f=True)
        for node in shapes:
            if f == 0:
                cmds.setAttr("{0}.overrideEnabled".format(node), 0)
                continue
            cmds.setAttr("{0}.overrideRGBColors".format(node), 1)
            cmds.setAttr("{0}.overrideEnabled".format(node), 1)
            cmds.setAttr("{0}.overrideColorRGB".format(node), r, g, b)


@dec_undo
def setIndexColor(index):
    selection = cmds.ls(sl=True)
    for select in selection:
        shapes = cmds.listRelatives(select, ad=True, s=True, f=True)
        for node in shapes:
            cmds.setAttr("{0}.overrideRGBColors".format(node), 0)
            if index == 0:
                cmds.setAttr("{0}.overrideEnabled".format(node), 0)
                continue
            cmds.setAttr("{0}.overrideEnabled".format(node), 1)
            cmds.setAttr("{0}.overrideColor".format(node), index)


def __fileWriteOrAdd(inFileName, inText, inWriteOption):
    if os.path.exists(inFileName):
        read_only_or_write_able = os.stat(inFileName)[0]
        if read_only_or_write_able != stat.S_IWRITE:
            os.chmod(inFileName, stat.S_IWRITE)

    file = open(inFileName, inWriteOption)
    file.write(inText)
    file.close()


def getMayaFonts():
    fontList = []
    fonts = cmds.fontDialog(FontList=True)
    for i in fonts:
        removed = i.split('-')
        fontList.append(removed[0])

    return _RemoveDuplicates(fontList)


def _RemoveDuplicates(seq):
    noDuplicates = []
    [noDuplicates.append(i) for i in seq if not noDuplicates.count(i)]
    return noDuplicates


def convertToIndexList(vertList):
    indices = []
    for i in vertList:
        index = int(i[i.index("[") + 1: -1])
        indices.append(index)
    return indices


def convertToCompList(indices, inMesh, comp="vtx"):
    vertices = []
    for i in list(indices):
        vrt = "%s.%s[%s]" % (inMesh, comp, i)

        vertices.append(vrt)
    return vertices


def convertToSeperateLoops(inFace):
    myNode = inFace.split(".")[0]
    allEdges = cmds.polyListComponentConversion(inFace, te=True)
    edges = cmds.filterExpand(allEdges, sm=32, fp=1)
    edgeSelection = []
    curves = []
    for edge in convertToIndexList(edges):
        edgeList = cmds.polySelect(myNode, q=1, edgeLoopOrBorder=edge)
        edgeList.sort()
        e = list(set(edgeList))
        if e in edgeSelection:
            continue
        edgeSelection.append(e)
        borderEdges = convertToCompList(e, myNode, "e")
        convertedVertices = cmds.polyListComponentConversion(borderEdges, tv=True)
        verts = cmds.filterExpand(convertedVertices, sm=31, fp=1)
        positions = [cmds.xform(vert, q=1, ws=1, t=1) for vert in verts]
        positions += [positions[0]]
        curves.append(cmds.curve(p=positions, d=1))
    return curves


def ByteToHex(byteStr):
    return ''.join(["%02X " % ord(x) for x in byteStr]).strip()


@dec_undo
def createTypeToolWithNode(nodeName, font=None, style=None, text=None):
    typeTool = cmds.createNode("type", n=nodeName)
    typeTransform = cmds.createNode('transform', n='%sMesh#' % nodeName, skipSelect=True)
    typeMesh = cmds.createNode('mesh', n='typeMeshShape#', p=typeTransform, skipSelect=True)
    cmds.connectAttr(typeTool + '.outputMesh', typeMesh + '.inMesh')

    if font is None:
        font = "Arial"
    if style is None:
        style = "Regular"

    cmds.setAttr(typeTool + '.currentFont', font, type="string")
    cmds.setAttr(typeTool + '.currentStyle', style, type="string")

    if text is None:
        text = nodeName
    cmds.setAttr(typeTool + ".textInput", ByteToHex(text), type="string")

    faces = cmds.ls("%s.f[*]" % typeMesh, fl=1)
    allCurves = []
    for face in faces:
        curves = convertToSeperateLoops(face)
        allCurves.extend(curves)

    cmds.delete(typeTool, typeTransform)
    return allCurves


def GetControler(inputCurve, curveDirectory, isChecked):
    cmds.delete(inputCurve, ch=True)

    directory = os.path.dirname(str(curveDirectory))
    if not os.path.exists(directory):
        os.makedirs(directory)

    baseText = 'import maya.cmds as cmds\n'
    __fileWriteOrAdd((curveDirectory), baseText, 'w')
    multipleShapes = False

    def completeList(input):
        childrenBase = cmds.listRelatives(input, ad=True, type="transform")
        childrenBase.append(input)
        childrenBase.reverse()
        return childrenBase

    childrenBase = cmds.listRelatives(inputCurve, ad=True, type="transform")
    if childrenBase:
        selection = completeList(inputCurve)
    else:
        selection = [inputCurve]

    for inputCurve in selection:
        shapeNode = cmds.listRelatives(inputCurve, s=True, f=True)
        listdef = '%s = []\n' % inputCurve
        __fileWriteOrAdd((curveDirectory), listdef, 'a')

        for shapes in shapeNode:
            controlVerts = cmds.getAttr(shapes + '.cv[*]')
            curveDegree = cmds.getAttr(shapes + '.degree')
            period = cmds.getAttr(shapes + '.f')
            localPosition = cmds.getAttr(inputCurve + '.translate')
            worldPosition = cmds.xform(inputCurve, q=True, piv=True, ws=True)

            infoNode = cmds.createNode('curveInfo')
            cmds.connectAttr((shapes + '.worldSpace'), (infoNode + '.inputCurve'))

            if len(shapeNode) > 1:
                multipleShapes = True

            list1 = []
            list2 = []
            list3 = []

            knots = cmds.getAttr(infoNode + '.knots')
            for i in knots[0]:
                list3.append(int(i))

            if isChecked:
                for i in range(len(controlVerts)):
                    for j in range(3):
                        originCalculation = (float(controlVerts[i][j]) - float(worldPosition[j]))
                        localSpaceAddition = originCalculation + float(localPosition[0][j])
                        list1.append(localSpaceAddition)
                    list2.append(list1)
                    list1 = []
            else:
                list2 = controlVerts

            if period == 0:
                periodNode = ',per = False'
            else:
                periodNode = ',per = True'
                for i in range(curveDegree):
                    list2.append(list2[i])

            _points = str(list2).replace('[', '(').replace(']', ')').replace('((', '[(').replace('))', ')]')
            _knots = str(list3)
            CurveCreation = 'cmds.curve( p ={0}{1}, d={2}, k={3})'.format(_points, periodNode, curveDegree, _knots)
            CurveCreation = '{0}.append({1})'.format(inputCurve, CurveCreation)
            __fileWriteOrAdd((curveDirectory), str(CurveCreation + '\n'), 'a')

            cmds.delete(infoNode)

        if multipleShapes == True:
            End = 'for x in range(len({0})-1):\n\tcmds.makeIdentity({0}[x+1], apply=True, t=1, r=1, s=1, n=0)\n\tshapeNode = cmds.listRelatives({0}[x+1], shapes=True)\n\tcmds.parent(shapeNode, {0}[0], add=True, s=True)\n\tcmds.delete({0}[x+1])\n'.format(inputCurve)
            __fileWriteOrAdd((curveDirectory), End, 'a')

        parentObject = cmds.listRelatives(inputCurve, parent=True)
        if parentObject:
            listdef = 'cmds.parent({0}[0], {1}[0])\n'.format(inputCurve, parentObject[0])
            __fileWriteOrAdd((curveDirectory), listdef, 'a')

    close = 'fp = cmds.listRelatives({0}[0], f=True)[0]\npath = fp.split("|")[1]\ncmds.select(path)'.format(inputCurve)
    __fileWriteOrAdd((curveDirectory), close, 'a')
