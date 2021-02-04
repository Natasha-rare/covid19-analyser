import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        # self.setFixedSize(1006, 807)
        self.show()
        self.loadBtn.clicked.connect(self.load)
        self.homeBtn.clicked.connect(self.home)
        self.settingsBtn.clicked.connect(self.settings)

    def home(self):
        uic.load('covid.ui', self)

    def settings(self):
        pass

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        filename = []
        if dialog.exec_():
            filename = dialog.selectedFiles()
        f = open(filename[0], 'r')
        with f:
            data = f.read()
            self.contents.setText(data)
        f.close()


app = QApplication(sys.argv)
ex = MyWidget()
# ex.show()
sys.exit(app.exec_())

