import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QLabel, QListWidget, QListWidgetItem
from home import HomeWindow

app = QApplication(sys.argv)
ex = HomeWindow()
ex.show()
sys.exit(app.exec_())
