import maya.cmds as mc


def validator_geometry_unlock(top_group):

    obj_list = mc.listRelatives(top_group, allDescendents=True, type="transform")

    for obj in obj_list:

        # Check attributes on the channelBox
        attr_list = mc.listAttr(obj, unlocked=False, keyable=True, visible=True)
        for attr in attr_list:

            # Define allowed attributes
            allowed_attrs = ["visibility", "translateX", "translateY", "translateZ",
                             "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]

            # If the attribute is not allowed, trigger a popup warning
            if attr not in allowed_attrs:
                # Show a popup dialog with a warning
                mc.confirmDialog(
                    title="Warning",
                    message="The attribute '{}' on '{}' should not be in the channelBox".format(attr, obj),
                    button=["OK"],
                    defaultButton="OK"
                )
            # If there is values on the channelBox attributes show popup warning

