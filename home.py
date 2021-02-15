import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QLabel, QListWidget, QListWidgetItem
from session import SessionWindow

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        self.show()
        self.loadBtn.clicked.connect(self.load)
        # self.settingsBtn.clicked.connect(self.settings)

    def settings(self):
        pass

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        filenames = []
        if dialog.exec_():
            filenames = dialog.selectedFiles()
        # TODO: check file type. If it is NIFTI, convert to PNG
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        # uic.loadUi('mainPage.ui', self)
        self.close()
        SessionWindow(filenames)
