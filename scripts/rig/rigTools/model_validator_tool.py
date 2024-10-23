import maya.cmds as mc


def validator_channelBox(top_group):
    obj_list = mc.listRelatives(top_group, allDescendents=True, type="transform")
    warning_message = ""
    for obj in obj_list:

        # Check attributes on the channelBox
        attr_list = mc.listAttr(obj, unlocked=False, keyable=True, visible=True)
        # Remove currentUVSet from the list
        attr_list = [attr for attr in attr_list if attr != "currentUVSet"]

        for attr in attr_list:

            # Define allowed attributes
            allowed_attrs = ["visibility", "translateX", "translateY", "translateZ",
                             "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]

            # If the attribute is not allowed
            if attr not in allowed_attrs:
                # Add title
                cb_attr_message = "-------------------------- Display Attribute Channel Box --------------------------"
                message = "The attribute '{}' on '{}' should not be on channelBox.".format(attr, obj)
                # Concatenate the warning message
                if not cb_attr_message in warning_message:
                    warning_message += cb_attr_message + "\n"
                warning_message += message + "\n"
                print(message)
            else:
                # If there is values on the channelBox attributes
                value = mc.attributeQuery(attr, node=obj, listDefault=True)[0]
                current_value = mc.getAttr("{}.{}".format(obj, attr))
                cb_attr_value_message = "--------------- Display Attribute Value Channel Box ---------------"
                message = "The attribute '{}' on '{}' has not default values.".format(attr, obj)
                # Concatenate the warning message
                if not cb_attr_value_message in warning_message:
                    warning_message += cb_attr_value_message + "\n"
                if value != current_value:
                    warning_message += message + "\n"
                print(obj + "." + attr + ": " + str(value))
        # Check pivot point on each geo
        scale_value = mc.xform(obj, query=True, worldSpace=True, scalePivot=True)
        rotate_value = mc.xform(obj, query=True, worldSpace=True, rotatePivot=True)
        print(rotate_value)
        print(scale_value)
        if scale_value != [0.0, 0.0, 0.0] or rotate_value != [0.0, 0.0, 0.0]:
            # Add title
            cb_attr_message = "-------------------------- Geometry Pivot --------------------------"
            message = "The geometry '{}' has not the pivot on the center of the scene.".format(obj)
            # Concatenate the warning message
            if not cb_attr_message in warning_message:
                warning_message += cb_attr_message + "\n"
            warning_message += message + "\n"
            print(message)
            print("Pivot is not on the center of the scene")
        else:
            print("Pivot is on the center of the scene")
    if warning_message:
        # Show a popup dialog with a warning
        mc.confirmDialog(
            title="Warning",
            message=warning_message,
            button=["OK"],
            messageAlign="Right",
            defaultButton="OK")
    # Check for geometry shapes only one.
    # Check no deformers on geometry.
    # Check pivot point is on 0,0,0.
    # Check name convention.


def run():
    tn = mc.ls(selection=True)[0]
    validator_channelBox(top_group=tn)
