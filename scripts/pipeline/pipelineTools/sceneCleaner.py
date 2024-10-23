import os
import maya.mel as mel


def scene_cleaner():
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

    # Select vars from 0 to 25
    select_vars = []
    for number in range(0, 25):
        select_vars.append(all_option_vars[number])

    # Convert select_vars to a MEL-compatible string format
    mel_select_vars = "{" + ", ".join([f'\"{var}\"' for var in select_vars]) + "}"

    # Cleanup
    if "MAYA_TESTING_CLEANUP" not in os.environ:
        os.environ["MAYA_TESTING_CLEANUP"] = "enable"
        mel.eval(f"scOpt_performOneCleanup({mel_select_vars})")
        del os.environ["MAYA_TESTING_CLEANUP"]
    else:
        mel.eval(f"scOpt_performOneCleanup({mel_select_vars})")


def run():
    scene_cleaner()
