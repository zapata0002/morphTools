import os
import maya.mel as mel

# Create list ("all_option_vars[]") for all cleanup options

all_option_vars = ["nurbsSrfOption",  # 0
                   "nurbsCrvOption",  # 1
                   "unusedNurbsSrfOption",  # 2
                   "locatorOption",  # 3
                   "clipOption",  # 4
                   "poseOption",  # 5
                   "ptConOption",  # 6
                   "pbOption",  # 7
                   "deformerOption",  # 8
                   "unusedSkinInfsOption",  # 9
                   "expressionOption",  # 10
                   "groupIDnOption",  # 11
                   "animationCurveOption",  # 12
                   "snapshotOption",  # 13
                   "unitConversionOption",  # 14
                   "shaderOption",  # 15
                   "cachedOption",  # 16
                   "transformOption",  # 17
                   "displayLayerOption",  # 18
                   "renderLayerOption",  # 19
                   "setsOption",  # 20
                   "partitionOption",  # 21
                   "referencedOption",  # 22
                   "brushOption",  # 23
                   "unknownNodesOption",  # 24
                   "shadingNetworksOption"  # 25
                   ]




# numeric_vars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 23, 25]

# Create string options list ("select_vars") for "numeric_vars" in "all_option_vars".
select_vars = []
for number in range(0,25): select_vars.append(all_option_vars[number])

# cleanup
mel.eval("all_option_vars = python(\"select_vars\")")
if "MAYA_TESTING_CLEANUP" not in os.environ:
    os.environ["MAYA_TESTING_CLEANUP"] = "enable"
    mel.eval("scOpt_performOneCleanup($select_vars)")
    del os.environ["MAYA_TESTING_CLEANUP"]
else:
    mel.eval("scOpt_performOneCleanup($select_vars)")
