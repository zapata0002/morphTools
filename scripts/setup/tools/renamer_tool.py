"""
Maya/QT UI template
Maya 2023
"""

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
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
        super(RenamerWindow, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = ('C:\\Users\\Usuario\\Documents\\maya\\scripts\\tools\\gui\\')
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + 'renamer_tool.ui')
        self.widget.setParent(self)
        original_width = self.widget.width()
        original_height = self.widget.height()
        self.setFixedSize(original_width, original_height)
        # locate UI widgets
        self.in_search = self.widget.findChild(QtWidgets.QLineEdit, 'in_search')
        self.in_replace = self.widget.findChild(QtWidgets.QLineEdit, 'in_replace')
        self.btn_searchReplace = self.widget.findChild(QtWidgets.QPushButton, 'btn_searchReplace')
        self.in_prefix = self.widget.findChild(QtWidgets.QLineEdit, 'in_prefix')
        self.btn_prefix = self.widget.findChild(QtWidgets.QPushButton, 'btn_prefix')
        self.in_suffix = self.widget.findChild(QtWidgets.QLineEdit, 'in_suffix')
        self.btn_suffix = self.widget.findChild(QtWidgets.QPushButton, 'btn_suffix')
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
        self.btn_clear.clicked.connect(self.clear)
        # get default values from the text lines
        self.search_default = self.in_search.text()
        self.replace_default = self.in_replace.text()
        self.prefix_default = self.in_prefix.text()
        self.suffix_default = self.in_suffix.text()
        self.orderRename_default = self.in_orderRename.text()
        self.orderStart_default = self.in_orderStart.text()
        self.orderPadding_default = self.in_orderPadding.text()
        self.orderPrefix_default = self.in_orderPrefix.text()
        self.orderSuffix_default = self.in_orderSuffix.text()
    """
    Your code goes here
    """
    def search_and_replace(self):
        cmds.undoInfo(openChunk=True)
        self.search_text = self.in_search.text()
        self.replace_text = self.in_replace.text()
        selected_list = cmds.ls(sl=True)
        if len(selected_list) == 0:
            cmds.warning("Select the node to replace")
        elif self.search_text == "":
            cmds.warning("Search entry field is empty")
        else:
            for sel in reversed(selected_list):
                split_name = sel.split('|')
                search_name_node = split_name[-1].replace(self.search_text, self.replace_text)
                cmds.rename(sel, search_name_node)
        cmds.undoInfo(closeChunk=True) 

    def add_prefix(self):
        cmds.undoInfo(openChunk=True)
        self.prefix_text = self.in_prefix.text()
        selected_list = cmds.ls(sl=True)
        if len(selected_list) == 0:
            cmds.warning("Select the node to add prefix")
        elif self.prefix_text == "":
            cmds.warning("Prefix entry field is empty")
        else:
            for sel in reversed(selected_list):
                split_name = sel.split('|')
                cmds.rename(sel, '{}{}'.format(self.prefix_text, split_name[-1]))
        cmds.undoInfo(closeChunk=True)

    def add_suffix(self):
        cmds.undoInfo(openChunk=True)
        selected_list = cmds.ls(sl=True)
        self.suffix_text = self.in_suffix.text()
        if len(selected_list) == 0:
            cmds.warning("Select the node to add suffix")
        elif self.suffix_text == "":
            cmds.warning("Suffix entry field is empty")
        else:
            for sel in reversed(selected_list):
                split_name = sel.split('|')
                cmds.rename(sel, '{}{}'.format(split_name[-1], self.suffix_text))
        cmds.undoInfo(closeChunk=True)

    def rename_and_order(self):
        cmds.undoInfo(openChunk=True)
        self.orderRename_text = self.in_orderRename.text()
        self.orderPrefix_text = self.in_orderPrefix.text()
        self.orderSuffix_text = self.in_orderSuffix.text()
        self.orderStart_text = self.in_orderStart.text()
        self.orderPadding_text = self.in_orderPadding.text()
        selected_list = cmds.ls(sl=True)
        if len(selected_list) == 0:
            cmds.warning("Select the node to rename")
        elif self.orderRename_text == "":
            cmds.warning("Rename entry field is empty")
        else:
            start_number = int(self.orderStart_text)
            padding_int = int(self.orderPadding_text)
            end_number = len(selected_list) + start_number - 1
            zero_padding = ''
            for sel in reversed(selected_list):
                end_number_len = len(str(end_number))
                if padding_int > end_number_len:
                    zero_padding = '0' * (padding_int - end_number_len)
                rename_name = cmds.rename(sel, '{}{}{}'.format(self.orderRename_text, zero_padding, str(end_number)))
                end_number -= 1
                if self.orderSuffix_text:
                    rename_name = cmds.rename(rename_name, '{}{}'.format(rename_name, self.orderSuffix_text))
                    if self.orderPrefix_text:
                        cmds.rename(rename_name, '{}{}'.format(self.orderPrefix_text, rename_name))
                else:
                    if self.orderPrefix_text:
                        cmds.rename(rename_name, '{}{}'.format(self.orderPrefix_text, rename_name))
            cmds.undoInfo(closeChunk=True)
    

    def clear(self):
        self.in_search.setText(self.search_default)
        self.in_replace.setText(self.replace_default)
        self.in_prefix.setText(self.prefix_default)
        self.in_suffix.setText(self.suffix_default)
        self.in_orderRename.setText(self.orderRename_default)
        self.in_orderPrefix.setText(self.orderPrefix_default)
        self.in_orderSuffix.setText(self.orderSuffix_default)
        self.in_orderStart.setText(self.orderStart_default)
        self.in_orderPadding.setText(self.orderPadding_default)


    def closeWindow(self):
        """
        Close window.
        """
        self.destroy()
    
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
    RenamerWindow.window = RenamerWindow(parent = mayaMainWindow)
    RenamerWindow.window.setObjectName('renamerTool') # code above uses this to ID any existing windows
    RenamerWindow.window.setWindowTitle('Renamer Tool')
    RenamerWindow.window.show()
    
openWindow()