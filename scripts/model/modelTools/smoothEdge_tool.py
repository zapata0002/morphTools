from maya import mel
import importlib
from scripts.model import modelMel

# Reload the modelMel module
importlib.reload(modelMel)

def run():
    # Define the tool_name and build the full path correctly
    tool_name = "smooth_wim_coene.mel"
    morphTools_path = "D:/repositories/morphTools/".replace("\\", "/")
    path = morphTools_path + "scripts/model/modelMel/" + tool_name  # Ensure the correct path

    # Use the full path in the MEL eval
    mel.eval(f'source "{path}";')

