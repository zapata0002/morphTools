import maya.cmds as mc


# Remove unused nodes on the scene
unused_nodes = [
    "mayaUsdLayerManager",
    "sequenceManager",
    "script",
    "shapeEditorManager",
    "trackInfoManager",
    "poseInterpolatorManager",
    "blendShape",
    "unknown",
    "aiAOVDriver",
    "aiAOVFilter",
    "aiOptions"
]


unused_list = mc.ls(type=unused_nodes)
if not unused_list :
    pass
else:
    for node in unused_list:
        if node in ["sequenceManager", "shapeEditorManager", "poseInterpolatorManager"]:
            print(node + " node can not be remove in the scene.")
        else:
            try:
                mc.delete(node)
                print("Delete: " + node)
            except:
                print("Deleted: " + node)
