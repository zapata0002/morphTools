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
                # Add title if not
                cb_attr_message = "----- Display Attribute Channel Box -----"
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
                cb_attr_value_message = "----- Display Attribute Value Channel Box -----"
                message = "The attribute '{}' on '{}' has not default values.".format(attr, obj)
                # Concatenate the warning message
                if not cb_attr_value_message in warning_message:
                    warning_message += cb_attr_value_message + "\n"
                if value != current_value:
                    warning_message += message + "\n"
                print(obj + "." + attr + ": " + str(value))

    if warning_message:
        # Show a popup dialog with a warning
        mc.confirmDialog(
            title="Warning",
            message=warning_message,
            button=["OK"],
            defaultButton="OK")
    # Check for geometry shapes only one.
    # Check no deformers on geometry.
    # Check pivot point is on 0,0,0.
    # Check name convention.

validator_channelBox(top_group="original")