from curveCreator.qt_util import *
import tempfile, os
from maya import cmds, OpenMayaUI


class CaptureWindow(QDialog):
    def __init__(self, parent=None, path='test'):
        super(CaptureWindow, self).__init__(parent)

        self.setLayout(QVBoxLayout())

        self.SaveAndCloseButton = QPushButton("Save And Close")
        self.vertLayoutWidget = QWidget(self)
        self.vertLayoutWidget.setGeometry(QRect(10, 10, 191, 201))
        self.vertLayoutWidget.setObjectName("vertLayoutWidget")
        self.layout().addWidget(self.vertLayoutWidget)
        self.layout().addWidget(self.SaveAndCloseButton)

        self.viewportLayout = QVBoxLayout(self.vertLayoutWidget)
        self.viewportLayout.setContentsMargins(0, 0, 0, 0)

        self.__itemCreated = False
        self.path = path
        self.cameraName = ''

        self.__addViewport()
        self.SaveAndCloseButton.clicked.connect(self.__saveAndClose)

    def __addViewport(self):
        self.cameraName = cmds.camera()[0]
        cmds.hide(self.cameraName)

        self.modelPanelName = cmds.modelEditor(camera=self.cameraName, displayAppearance='smoothShaded', dtx=0, hud=0, alo=0, nc=1, grid=0)

        ptr = OpenMayaUI.MQtUtil.findControl(self.modelPanelName)
        self.modelEditor = wrapinstance(long(ptr))
        self.viewportLayout.addWidget(self.modelEditor)

        cmds.viewFit(self.cameraName, all=True)

    def createSnapshot(self):
        filePath = os.path.join(tempfile.gettempdir(), 'screenshot.png')
        if os.path.isdir(os.path.dirname(self.path)):
            filePath = self.path
        print(filePath)
        QPixmap.grabWindow(self.modelEditor.winId()).save(filePath)
        self.__itemCreated = filePath
        return filePath

    def __saveAndClose(self, *args):
        self.createSnapshot()
        self.close()
        self.deleteLater()

    def returnCreatedItem(self):
        return self.__itemCreated

    def hideEvent(self, event):
        QDialog.hideEvent(self, event)
        cmds.delete(self.cameraName)


def testUI():
    window_name = 'captureWindowTest'
    mainWindow = get_maya_window()

    if mainWindow:
        for child in mainWindow.children():
            if child.objectName() == window_name:
                child.close()
                child.deleteLater()
    window = CaptureWindow(mainWindow)
    window.setObjectName(window_name)
    window.setWindowTitle(window_name)
    window.setFixedSize(QSize(300, 400))
    window.exec_()

    return window
