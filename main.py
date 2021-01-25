import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        # self.setFixedSize(1006, 807)
        self.show()

app = QApplication(sys.argv)
ex = MyWidget()
# ex.show()
sys.exit(app.exec_())

