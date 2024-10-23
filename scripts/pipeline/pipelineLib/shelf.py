from maya import cmds as mc
import importlib
from scripts.rig.rigTools import renamer_tool_100 as renamer_tool
importlib.reload(renamer_tool)


def customPopupMenu(name, script_list):
    # Check if the popup menu already exists and delete it
    if mc.popupMenu(name, exists=True):
        mc.deleteUI(name, menu=True)
    else:
        # Create a new popup menu
        popup = mc.popupMenu(name, button=1)
        # Add menu items
        for script in script_list:
            if mc.menuItem(script, exists=True):
                mc.deleteUI(script)
            else:
                mc.menuItem(label=script, command=lambda *args: print(f"{script} Selected"))


def utilsPopupMenu():
    script_list = ["Renamer"]
    customPopupMenu(name="Utils", script_list=script_list)
    for script in script_list:
        if script == "Renamer":
            script = renamer_tool.run()
            mc.menuItem(label=script, command=renamer_tool.run())


"""
# Load renamer tool

import sys
import os
import importlib

path = 'D:\\repositories\\morphTools\\'
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)


from scripts.pipeline.pipelineLib import shelf


# Ensure the button exists, then create or update it
# button_name = 'myPopupButton'
buttons_list = ["Geometry", "Selection", "Curve", "Deformers", "Controls", "Connection", "Utils"]
shelf_name = 'ZapataShelf'  # Ensure this matches an existing shelf


for btn in buttons_list:
    print(btn)
    # Delete the button if it already exists (to prevent duplicates)
    if mc.shelfButton(btn, exists=True):
        mc.deleteUI(btn)
    # Create the shelf button
    if btn == "Geometry":
        name = "Geometry"
        label_list = ["Option 1", "Option 2", "Option 3"]
        mc.shelfButton(btn, label=btn, parent=shelf_name, command=shelf.customPopupMenu(name=name, label_list=label_list))
    else:
        pass
"""

