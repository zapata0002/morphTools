from maya import mel
import importlib
from scripts.pipeline import pipelineMel

# Reload the modelMel module
importlib.reload(pipelineMel)


def run():
    # Define the tool_name and build the full path correctly
    tool_name = "abSymMesh.mel"
    morphTools_path = "D:/repositories/morphTools/".replace("\\", "/")
    path = morphTools_path + "scripts/pipeline/pipelineMel/" + tool_name  # Ensure the correct path

    # Use the full path in the MEL eval
    mel.eval(f'source "{path}";')

