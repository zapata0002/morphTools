import maya.cmds as cmds


def customPopupMenu(*args):
    # Check if the popup menu already exists and delete it
    if cmds.popupMenu('myPopupMenu', exists=True):
        cmds.deleteUI('myPopupMenu', menu=True)

    # Create a new popup menu
    popup = cmds.popupMenu('myPopupMenu', button=1)

    # Add menu items
    cmds.menuItem(label='Option 1', command=lambda *args: print("Option 1 Selected"))
    cmds.menuItem(label='Option 2', command=lambda *args: print("Option 2 Selected"))
    cmds.menuItem(label='Option 3', command=lambda *args: print("Option 3 Selected"))


# Ensure the button exists, then create or update it
button_name = 'myPopupButton'
shelf_name = 'ZapataShelf'  # Ensure this matches an existing shelf

# Delete the button if it already exists (to prevent duplicates)
if cmds.shelfButton(button_name, exists=True):
    cmds.deleteUI(button_name)

# Create the shelf button
cmds.shelfButton(button_name, label='My Popup', parent=shelf_name, command='customPopupMenu()')
