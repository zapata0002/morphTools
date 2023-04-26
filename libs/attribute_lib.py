# Maya imports
from maya import cmds

class Helper(object):
    def __init__(self, name):
        """
        :param name: str, node's name
        """
        self.name = name

    # ---------- Checks Methods ----------
    def check_attribute_exists(self, attribute_name):
        """
        Check if the attribute's name exists in the node
        :param attribute_name: str
        :return: bool
        """
        if cmds.attributeQuery(attribute_name, node=self.name, exists=True):
            return True
        else:
            return False

    # ---------- Set methods ----------
    def lock_attribute(self, attribute_name, lock=True):
        """
        Lock an attribute
        :param attribute_name: str
        :param lock: bool
        """
        if cmds.getAttr('{}.{}'.format(self.name, attribute_name), settable=True):
            cmds.setAttr('{}.{}'.format(self.name, attribute_name), lock=lock)

    def lock_attributes(self, attributes_list, lock=True):
        """
        Lock the attributes' list
        :param attributes_list: list
        :param lock: bool
        :return:
        """
        for attr in attributes_list:
            self.lock_attribute(attr, lock=lock)

    def hide_attribute(self, attribute_name, hide=True):
        """
        Hide an attribute
        :param attribute_name: str
        :param hide: bool
        """
        cmds.setAttr('{}.{}'.format(self.name, attribute_name), keyable=not hide, channelBox=not hide)

    def hide_attributes(self, attributes_list, hide=True):
        """
        Hide the attributes' list
        :param attributes_list: list
        :param hide: bool
        """
        for attr in attributes_list:
            self.hide_attribute(attr, hide=hide)

    def lock_and_hide_attribute(self, attribute_name, lock=True, hide=True):
        """
        Lock and hide an attribute
        :param attribute_name: str
        :param lock: bool
        :param hide: bool
        """
        self.lock_attribute(attribute_name, lock)
        self.hide_attribute(attribute_name, hide)

    def lock_and_hide_attributes(self, attributes_list, lock=True, hide=True):
        """
        Lock and hide the attributes' list
        :param attributes_list: list
        :param lock: bool
        :param hide: bool
        """
        for attr in attributes_list:
            self.lock_and_hide_attribute(attr, lock, hide)

    def keyable_attribute(self, attribute_name, keyable=True):
        """
        Change attribute property between keyable and not keyable
        :param attribute_name: str
        :param keyable: bool
        """
        cmds.setAttr('{}.{}'.format(self.name, attribute_name), keyable=keyable, channelBox=not keyable)

    def set_default_value(self, attr, value):
        cmds.addAttr('{}.{}'.format(self.name, attr), edit=True, defaultValue=value)
        cmds.setAttr('{}.{}'.format(self.name, attr), value)

    # ---------- Add attributes Methods ----------
    def add_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        Add an attribute to the node
        :param attribute_name: str
        :param keyable: bool
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name
        """
        if self.check_attribute_exists(attribute_name):
            cmds.warning('{}.{} already exists'.format(self.name, attribute_name))
        else:
            cmds.addAttr(self.name, longName=attribute_name, **kwargs)
            cmds.setAttr('{}.{}'.format(self.name, attribute_name), keyable=keyable, channelBox=not keyable)

        return attribute_name

    def add_separator_attribute(self, separator_name):
        """
        Add a separator in the attributes
        :param separator_name: str
        :return: separator name
        """
        if not cmds.attributeQuery(separator_name, node=self.name, exists=True):
            self.add_attribute(separator_name, niceName=' ', attributeType='enum',
                               enumName=separator_name)
            self.keyable_attribute(separator_name, keyable=False)

        return separator_name

    def add_float_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        add a float attribute
        :param attribute_name: str
        :param keyable: bool
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name
        """
        return self.add_attribute(attribute_name, attributeType='float', keyable=keyable, **kwargs)

    def add_int_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        add a integer attribute
        :param attribute_name: str
        :param keyable: bool
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name
        """
        return self.add_attribute(attribute_name, attributeType='long', keyable=keyable, **kwargs)

    def add_bool_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        add a bool attribute
        :param attribute_name: str
        :param keyable: bool
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name
        """
        return self.add_attribute(attribute_name, attributeType='bool', keyable=keyable, **kwargs)

    def add_enum_attribute(self, attribute_name, states, keyable=True, **kwargs):
        """
        add a enum attribute
        :param states: str, separate the values with ":"
        :param attribute_name: str
        :param keyable: bool
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name
        """
        return self.add_attribute(attribute_name, attributeType='enum', enumName=states, keyable=keyable, **kwargs)

    def add_proxy_attribute(self, attribute_name, node_attribute_proxy):
        """
        Add a proxy attribute
        :param attribute_name: str
        :param node_attribute_proxy:str,  node with the attribute
        :return: attribute's name
        """
        cmds.addAttr(self.name, longName=attribute_name, proxy=node_attribute_proxy)

        return attribute_name

    def add_matrix_attribute(self, attribute_name, **kwargs):
        """
        Add a matrix attribute
        :param attribute_name: str
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name
        """
        return self.add_attribute(attribute_name, attributeType='matrix', **kwargs)

    def add_string_attribute(self, attribute_name, text):
        """
        Add a matrix attribute
        :param attribute_name: str
        :param text: str
        :return: attribute's name
        """
        self.add_attribute(attribute_name, dataType='string')
        cmds.setAttr('{}.{}'.format(self.name, attribute_name), text, type='string')
        return attribute_name

    def global_scale_attribute(self, attribute_name='globalScale'):
        """
        Add a global scale attribute
        :param attribute_name: str
        :return: attribute's name
        """
        global_scale_attr = self.add_float_attribute(attribute_name, keyable=True, minValue=0.01, defaultValue=1)
        for axis in ['X', 'Y', 'Z']:
            cmds.connectAttr('{}.{}'.format(self.name, attribute_name),
                             '{}.scale.scale{}'.format(self.name, axis), force=True)
            self.hide_attribute(attribute_name='scale.scale{}'.format(axis), hide=True)
        return global_scale_attr

    # ---------- Get attributes Methods ----------
    def get_user_defined_attributes(self):
        """
        Get the attributes generated by the user
        :return: user defined attributes' list
        """
        return cmds.listAttr(self.name, userDefined=True, settable=True)
