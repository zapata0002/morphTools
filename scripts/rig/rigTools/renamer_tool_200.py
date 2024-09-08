import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial  # optional, for passing args during signal function calls
import sys


class RenamerWindow(QtWidgets.QWidget):
    """
    Create a default tool window.
    """
    window = None

    def __init__(self, parent = None):
        """
        Initialize class.
        """
        super(RenamerWindow, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = 'D:\\repositories\\morphTools\\scripts\\rig\\rigTools\\gui\\'
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + 'renamer_tool_2.0.ui')
        self.widget.setParent(self)
        original_width = self.widget.width()
        original_height = self.widget.height()
        print(original_width, original_height)
        # Set the window size and prevent resizing
        self.resize(original_width, original_height)
        self.setMinimumSize(original_width, original_height)
        self.setMaximumSize(original_width, original_height)

        # locate UI widgets
        self.in_search = self.widget.findChild(QtWidgets.QLineEdit, 'in_search')
        self.in_replace = self.widget.findChild(QtWidgets.QLineEdit, 'in_replace')
        self.btn_searchReplace = self.widget.findChild(QtWidgets.QPushButton, 'btn_searchReplace')
        self.in_prefix = self.widget.findChild(QtWidgets.QLineEdit, 'in_prefix')
        self.btn_prefix = self.widget.findChild(QtWidgets.QPushButton, 'btn_prefix')
        self.in_suffix = self.widget.findChild(QtWidgets.QLineEdit, 'in_suffix')
        self.btn_suffix = self.widget.findChild(QtWidgets.QPushButton, 'btn_suffix')
        self.rbtn_orderNum = self.widget.findChild(QtWidgets.QRadioButton, 'rbtn_orderNum')
        self.rbtn_orderLetter = self.widget.findChild(QtWidgets.QRadioButton, 'rbtn_orderLetter')
        self.in_orderRename = self.widget.findChild(QtWidgets.QLineEdit, 'in_orderRename')
        self.in_orderPrefix = self.widget.findChild(QtWidgets.QLineEdit, 'in_orderPrefix')
        self.in_orderSuffix = self.widget.findChild(QtWidgets.QLineEdit, 'in_orderSuffix')
        self.in_orderStart = self.widget.findChild(QtWidgets.QLineEdit, 'in_orderStart')
        self.in_orderPadding = self.widget.findChild(QtWidgets.QLineEdit, 'in_orderPadding')
        self.btn_orderRename = self.widget.findChild(QtWidgets.QPushButton, 'btn_orderRename')
        self.btn_clear = self.widget.findChild(QtWidgets.QPushButton, 'btn_clear')
        # assign functionality to buttons
        self.btn_searchReplace.clicked.connect(self.search_and_replace)
        self.btn_prefix.clicked.connect(self.add_prefix)
        self.btn_suffix.clicked.connect(self.add_suffix)
        self.btn_orderRename.clicked.connect(self.rename_and_order)
        # self.btn_clear.clicked.connect(self.clear)
        # get default values from the text lines
        self.search_default = self.in_search.text()
        self.replace_default = self.in_replace.text()
        self.prefix_default = self.in_prefix.text()
        self.suffix_default = self.in_suffix.text()
        self.orderNum_default = self.rbtn_orderNum.isChecked()
        self.orderLetter_default = self.rbtn_orderLetter.isChecked()
        self.orderRename_default = self.in_orderRename.text()
        self.orderStart_default = self.in_orderStart.text()
        self.orderPadding_default = self.in_orderPadding.text()
        self.orderPrefix_default = self.in_orderPrefix.text()
        self.orderSuffix_default = self.in_orderSuffix.text()
        # Connect radio button toggled signals to the slot
        self.rbtn_orderLetter.toggled.connect(self.update_padding_lock)
        self.rbtn_orderNum.toggled.connect(self.update_padding_lock)

    def search_and_replace(self):
        cmds.undoInfo(openChunk=True)
        search_text = self.in_search.text()
        replace_text = self.in_replace.text()
        # print(search_text, replace_text)
        selected_list = cmds.ls(sl=True)
        if len(selected_list) == 0:
            cmds.warning("Select the node to replace")
        elif search_text == "":
            cmds.warning("Search entry field is empty")
        else:
            for sel in reversed(selected_list):
                # print(sel)
                if "|" in sel:
                    split_name = sel.split('|')[-1]
                    search_name_node = split_name.replace(search_text, replace_text)
                    # print(search_name_node)
                else:
                    search_name_node = sel.replace(search_text, replace_text)
                    # print(search_name_node)
                cmds.rename(sel, search_name_node)
        cmds.undoInfo(closeChunk=True)

    def add_prefix(self):
        cmds.undoInfo(openChunk=True)
        prefix_text = self.in_prefix.text()
        selected_list = cmds.ls(sl=True)
        if len(selected_list) == 0:
            cmds.warning("Select the node to add prefix")
        elif prefix_text == "":
            cmds.warning("Prefix entry field is empty")
        else:
            for sel in reversed(selected_list):
                split_name = sel.split('|')
                cmds.rename(sel, '{}{}'.format(prefix_text, split_name[-1]))
        cmds.undoInfo(closeChunk=True)

    def add_suffix(self):
        cmds.undoInfo(openChunk=True)
        selected_list = cmds.ls(sl=True)
        suffix_text = self.in_suffix.text()
        if len(selected_list) == 0:
            cmds.warning("Select the node to add suffix")
        elif suffix_text == "":
            cmds.warning("Suffix entry field is empty")
        else:
            for sel in reversed(selected_list):
                split_name = sel.split('|')
                cmds.rename(sel, '{}{}'.format(split_name[-1], suffix_text))
        cmds.undoInfo(closeChunk=True)

    def rename_and_order(self):
        cmds.undoInfo(openChunk=True)

        orderRename_text = self.in_orderRename.text()
        orderPrefix_text = self.in_orderPrefix.text()
        orderSuffix_text = self.in_orderSuffix.text()
        orderStart_text = self.in_orderStart.text()
        orderPadding_text = self.in_orderPadding.text()
        selected_list = cmds.ls(sl=True)
        if len(selected_list) == 0:
            cmds.warning("Select the node to rename")
        elif orderRename_text == "":
            cmds.warning("Rename entry field is empty")
        else:
            if self.rbtn_orderNum.isChecked() is True:
                start_number = int(orderStart_text)
                padding_int = int(orderPadding_text)
                end_number = len(selected_list) + start_number - 1
                zero_padding = ''
                for sel in reversed(selected_list):
                    end_number_len = len(str(end_number))
                    if padding_int > end_number_len:
                        zero_padding = '0' * (padding_int - end_number_len)
                    rename_name = cmds.rename(sel, '{}{}{}'.format(orderRename_text, zero_padding, str(end_number)))
                    end_number -= 1
                    if orderSuffix_text:
                        rename_name = cmds.rename(rename_name, '{}{}'.format(rename_name, orderSuffix_text))
                        if orderPrefix_text:
                            cmds.rename(rename_name, '{}{}'.format(orderPrefix_text, rename_name))
                    else:
                        if orderPrefix_text:
                            cmds.rename(rename_name, '{}{}'.format(orderPrefix_text, rename_name))
            elif self.rbtn_orderLetter.isChecked() is True:
                orderOption = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                start_letter_index = int(orderStart_text) - 1
                # We don't use padding for letters
                current_index = start_letter_index

                for sel in selected_list:
                    # Convert index into letter
                    letter_parts = []
                    temp_index = current_index
                    while temp_index >= 0:
                        # remainder(resto) = dividend % divisor
                        letter_parts.append(orderOption[temp_index % len(orderOption)])
                        # quotient(coefficient) = dividend // divisor and integer operation
                        temp_index = temp_index // len(orderOption) - 1

                    # Build letter structure
                    current_letter = ''.join(reversed(letter_parts))
                    print("Current letter: " + current_letter)

                    rename_name = cmds.rename(sel, '{}{}'.format(orderRename_text, current_letter))
                    # Grow index for next
                    current_index += 1

                    if orderSuffix_text:
                        rename_name = cmds.rename(rename_name, '{}{}'.format(rename_name, orderSuffix_text))
                        if orderPrefix_text:
                            cmds.rename(rename_name, '{}{}'.format(orderPrefix_text, rename_name))
                    else:
                        if orderPrefix_text:
                            cmds.rename(rename_name, '{}{}'.format(orderPrefix_text, rename_name))

            else:
                cmds.warning("No order option checked, choose between number or letter")

            cmds.undoInfo(closeChunk=True)

    def clear(self):
        self.in_search.setText(self.search_default)
        self.in_replace.setText(self.replace_default)
        self.in_prefix.setText(self.prefix_default)
        self.in_suffix.setText(self.suffix_default)
        self.rbtn_orderNum.setChecked(self.orderNum_default)
        self.rbtn_orderLetter.setChecked(self.orderLetter_default)
        self.in_orderRename.setText(self.orderRename_default)
        self.in_orderPrefix.setText(self.orderPrefix_default)
        self.in_orderSuffix.setText(self.orderSuffix_default)
        self.in_orderStart.setText(self.orderStart_default)
        self.in_orderPadding.setText(self.orderPadding_default)

    def update_padding_lock(self):
        # Enable or disable QLineEdit based on the state of the radio buttons
        if self.rbtn_orderLetter.isChecked():
            self.in_orderPadding.setEnabled(False)
        else:
            self.in_orderPadding.setEnabled(True)


def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'renamerTool' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    RenamerWindow.window = RenamerWindow(parent=mayaMainWindow)
    RenamerWindow.window.setObjectName('renamerTool')  # code above uses this to ID any existing windows
    RenamerWindow.window.setWindowTitle('Renamer Tool')
    RenamerWindow.window.show()


def run():
    openWindow()


