# -*- coding: utf-8 -*-
QT_VERSION = "none"
ERROR_LIST = {}
from curveCreator.py23 import *
import re, json, os
UIDIRECTORY = os.path.dirname(__file__)
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtCore import Signal as pyqtSignal
    from PySide.QtSvg import *
    from PySide import QtGui
    from PySide.QtUiTools import *
    import sip

    QString = None
    QT_VERSION = "pyside"
except Exception as e:
    ERROR_LIST["Pyside import"] = e
    try:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
        from PySide2.QtCore import Signal as pyqtSignal
        from PySide2.QtSvg import *
        from PySide2 import QtGui
        from PySide2.QtUiTools import *
        import shiboken2 as shiboken

        QString = None
        QT_VERSION = "pyside2"
    except Exception as e:
        ERROR_LIST["Pyside2 import"] = e
        try:
            from PyQt4.QtCore import *
            from PyQt4.QtGui import *
            from PyQt4.QtSvg import *
            from PyQt4 import QtGui
            from PyQt4.QtUiTools import *
            import shiboken

            QT_VERSION = "pyqt4"
        except Exception as e:
            ERROR_LIST["PyQt4 import"] = e

if QT_VERSION == "none":
    for version in ERROR_LIST.keys():
        print(version, ERROR_LIST[version])


nameRegExp = QRegExp('\\w+')


def wrapinstance(ptr, base=None):
    '''workaround to be able to wrap objects with both PySide and PyQt4'''
    # http://nathanhorne.com/?p=485'''
    if ptr is None:
        return None
    ptr = int(ptr)
    if 'shiboken' in globals().keys():
        if base is None:
            qObj = shiboken.wrapInstance(int(ptr), QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QWidget
        return shiboken.wrapInstance(int(ptr), base)
    elif "sip" in globals().keys():
        base = QObject
        return sip.wrapinstance(int(ptr), base)
    else:
        return None


def get_maya_window():
    for widget in QApplication.allWidgets():
        try:
            if widget.objectName() == "MayaWindow":
                return widget
        except:
            pass
    return None


def nullLayout(inType, parent=None, size=0):
    v = inType()
    v.setContentsMargins(size, size, size, size)
    return v


def QuickDialog(title):
    """ convenience Quick dialog for simple accept and reject functions

    :param title: title for the dialog
    :type title: string
    :return: the window to be created
    :rtype: QDialog
    """
    myWindow = QDialog()
    myWindow.setWindowTitle(title)
    myWindow.setLayout(nullVBoxLayout())
    h = nullHBoxLayout()
    myWindow.layout().addLayout(h)
    btn = pushButton("Accept")
    btn.clicked.connect(myWindow.accept)
    h.addWidget(btn)
    btn = pushButton("Reject")
    btn.clicked.connect(myWindow.reject)
    h.addWidget(btn)
    return myWindow


def pushButton(text=''):
    """ simple button command with correct stylesheet

    :param text: text to add to the button
    :type text: string
    :return: the button  
    :rtype: QPushButton
    """
    btn = QPushButton(text)
    btn.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #595959, stop:1 #444444);")
    return btn


def buttonsToAttach(name, command, *_):
    """ convenience function to attach signal command to qpushbutton on creation

    :param name: text to add to the button
    :type name: string
    :param command: python command to attach to the current button on clicked signal
    :type command: <function>
    :return: the button  
    :rtype: QPushButton
    """
    button = pushButton()

    button.setText(name)
    button.setObjectName(name)

    button.clicked.connect(command)
    button.setMinimumHeight(23)
    return button


def svgButton(name='', pixmap='', size=None, toolTipInfo=None):
    """ toolbutton function with image from svg file

    :param name: text to add to the button
    :type name: string
    :param pixmap: location of the svg file
    :type pixmap: string
    :param size: height and width of image in pixels
    :type size: int
    :return: the button  
    :rtype: QPushButton
    """
    btn = QPushButton(name.lower())
    btn.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #595959, stop:1 #444444);")
    if name != '':
        btn.setLayoutDirection(Qt.LeftToRight)
        btn.setStyleSheet("QPushButton { text-align: left; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #595959, stop:1 #444444); }")
    _empty = False
    if isinstance(pixmap, str):
        if "empty" in pixmap.lower():
            _empty = True
        pixmap = QPixmap(pixmap)
    btn.setIcon(QIcon(pixmap))
    btn.setFocusPolicy(Qt.NoFocus)
    if not toolTipInfo is None:
        btn.setWhatsThis(toolTipInfo)

    if size is not None:
        _size = QSize(size, size)
        btn.setIconSize(_size)
    return btn


def toolButton(pixmap='', orientation=0, size=None):
    """ toolbutton function with image

    :param pixmap: location of the image
    :type pixmap: string
    :param orientation: rotation in degrees clockwise
    :type orientation: int
    :param size: height and width of image in pixels
    :type size: int
    :return: the button  
    :rtype: QToolButton
    """
    btn = QToolButton()
    if isinstance(pixmap, str):
        pixmap = QPixmap(pixmap)
    if orientation != 0 and not _isSVG:
        transform = QTransform().rotate(orientation, Qt.ZAxis)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
    btn.setIcon(QIcon(pixmap))
    btn.setFocusPolicy(Qt.NoFocus)
    btn.setStyleSheet('border: 0px;')
    if size is not None:
        if type(size) == int:
            btn.setFixedSize(QSize(size, size))
            btn.setIconSize(QSize(size, size))
        else:
            btn.setFixedSize(size)
            btn.setIconSize(size)
    return btn


def loadLanguageFile(language, widgetName):
    """ load the language file based on given inputs

    :param language: the language used in the dictionary
    :type language: string
    :param widgetName: name of the widget used to link the language file with
    :type widgetName: string
    :return: the translation dictionary
    :rtype: dict
    """
    languagesDir = os.path.join(UIDIRECTORY, "languages")
    curLangDir = os.path.join(languagesDir, language)
    if not os.path.exists(curLangDir):
        print("no language (%s) folder found for widget <%s>!" % (language, widgetName))
        return False

    widgetLanguageFile = os.path.join(curLangDir, "%s.LAN" % widgetName)
    if not os.path.exists(widgetLanguageFile):
        print("no language (%s) file found for widget <%s>!" % (language, widgetName))
        return False

    with open(widgetLanguageFile) as f:
        _data = json.load(f)
    return _data


def FalseFolderCharacters(inString):
    """ checking a string for characters that are not allowed in folder structures

    :param inString: the string to check
    :type inString: string
    :return: if the string has bad characters
    :rtype: bool
    """
    return re.search(r'[\\/:\[\]<>"!@#$%^&-.]', inString) or re.search(r'[*?|]', inString) or re.match(r'[0-9]', inString) or re.search(u'[\u4E00-\u9FFF]+', inString, re.U) or re.search(u'[\u3040-\u309Fー]+', inString, re.U) or re.search(u'[\u30A0-\u30FF]+', inString, re.U)


def FalseFolderCharactersJapanese(self, inString):
    """ checking a string for characters that are not allowed in folder structures

    :param inString: the string to check
    :type inString: string
    :return: if the string has bad characters
    :rtype: bool
    """
    return re.search(r'[\\/:\[\]<>"!@#$%^&-]', inString) or re.search(r'[*?|]', inString) or "." in inString or (len(inString) > 0 and inString[0].isdigit()) or re.search(u'[\u4E00-\u9FFF]+', inString, re.U) or re.search(u'[\u3040-\u309Fー]+', inString, re.U) or re.search(u'[\u30A0-\u30FF]+', inString, re.U)


def setProgress(inValue, progressBar=None, inText=''):
    """ convenience function to set the progress bar value even when a qProgressbar does not exist

    :param inValue: the current percentage of the progressbar
    :type inValue: int
    :param progressbar: the progressbar to update
    :type progressbar: QProgressBar
    :param inText: additional text to show with the progressbar
    :type inText: string
    """
    if progressBar is False:
        return
    if progressBar is None:
        from SkinningTools.Maya import api
        api.textProgressBar(inValue, inText)
        return
    progressBar.message = inText
    progressBar.setValue(inValue)
    QApplication.processEvents()


class LineEdit(QLineEdit):
    """override the focus steal on the lineedit"""
    allowText = pyqtSignal(bool)

    def __init__(self, folderSpecific=True, *args):
        super(LineEdit, self).__init__(*args)
        self.__qt_normal_color = QPalette(self.palette()).color(QPalette.Base)

        if folderSpecific:
            self.textChanged[unicode].connect(self._checkString)

    def __lineEdit_Color(self, inColor):
        PalleteColor = QPalette(self.palette())
        PalleteColor.setColor(QPalette.Base, QColor(inColor))
        self.setPalette(PalleteColor)

    def _checkString(self):
        _curText = self.displayText()
        if FalseFolderCharacters(_curText) != None:
            self.__lineEdit_Color('red')
            self.allowText.emit(False)
        else:
            self.__lineEdit_Color(self.__qt_normal_color)
            self.allowText.emit(True)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Control or key == Qt.Key.Key_Shift:
            return
        else:
            super(self.__class__, self).keyPressEvent(event)


class ColorPicker(QColorDialog):
    def __init__(self, *args):
        super(ColorPicker, self).__init__(*args)
        self.setOptions(QColorDialog.NoButtons | QColorDialog.DontUseNativeDialog)

        widgets = self.findChildren(QWidget)

        mainLayout = self.layout()
        hboxLayout = nullLayout(QHBoxLayout, None, 0)
        mainLayout.insertLayout(0, hboxLayout)
        vboxLayout = nullLayout(QVBoxLayout, None, 0)
        hboxLayout.addLayout(vboxLayout)
        vboxLayout.addWidget(widgets[9])
        vboxLayout.addWidget(widgets[2])
        hboxLayout.addWidget(widgets[7])

        for i in [0, 1, 3, 4, 5, 6]:
            widgets[i].hide()
