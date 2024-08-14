import maya.cmds as mc

# Define the RGB values for the colors
color_rgb = {
    "blue": (173, 216, 230),
    "crimson": (220, 20, 60),
    "cyan": (224, 255, 255),
    "green": (144, 238, 144),
    "lime": (191, 255, 193),
    "magenta": (255, 182, 193),
    "orange": (255, 179, 71),
    "red": (255, 105, 97),
    "teal": (175, 238, 238),
    "turquoise": (175, 238, 238),
    "violet": (238, 130, 238),
    "yellow": (255, 255, 224),
    "grey": (211, 211, 211)
}

# Define the value indices and their corresponding multipliers for brightness
valueIndex = ["020", "040", "060", "080", "100", "120", "140", "160", "180"]
multipliers = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]

# Create Lambert shaders in Maya
for color, rgb in color_rgb.items():
    for val, multiplier in zip(valueIndex, multipliers):
        # Scale RGB values based on multiplier and mix with white (255, 255, 255)
        scaled_rgb = tuple(int((component * multiplier + 255) / 2) for component in rgb)

        matName = "landmark_{}{}".format(color, val)
        lambert_shader = mc.shadingNode('lambert', asShader=True, name="{}".format(matName))

        # Set shader attributes
        mc.setAttr("{}.color".format(lambert_shader), scaled_rgb[0] / 255.0, scaled_rgb[1] / 255.0,
                   scaled_rgb[2] / 255.0, type="double3")
        mc.setAttr("{}.transparency".format(lambert_shader), 0.0, 0.0, 0.0, type="double3")
        mc.setAttr("{}.ambientColor".format(lambert_shader), 0.0, 0.0, 0.0, type="double3")
        mc.setAttr("{}.incandescence".format(lambert_shader), 0.0, 0.0, 0.0, type="double3")
        mc.setAttr("{}.diffuse".format(lambert_shader), 0.8)

        print("Created Lambert shader:", lambert_shader)
