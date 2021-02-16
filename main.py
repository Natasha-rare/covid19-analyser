import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QLabel, QListWidget, QListWidgetItem
from PIL import Image
import shutil
import os
import torch
import requests, cv2, tqdm, torchvision, yaml, matplotlib, pandas, seaborn


class MainWindow(QMainWindow):
    def __init__(self, filenames=None, results__dir_index=None, parent=None):
        super().__init__(parent)
        self.results_index = results__dir_index
        uic.loadUi('mainPage.ui', self)
        self.analyze(filenames)
        self.openResults(os.listdir(f'results{self.results_index}'))
        self.setFixedSize(800, 600)
        self.setWindowTitle(f'Session {self.results_index}')

    def analyze(self, filenames):
        print('LOADING MODEL:')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path_or_model=f'{os.getcwd()}/best.pt')
        images = []
        for img in filenames:
            images.append(Image.open(img))
        results = self.model(images, size=256)
        results.print()
        if not os.path.exists(f'results{self.results_index}'):
            os.mkdir(f'results{self.results_index}')
        results.save(f'results{self.results_index}')

    def illness_check(self, image_path):
        img = cv2.imread(f'{os.getcwd()}/results{self.results_index}/{image_path}')
        if len(img.shape) < 3:
            return False
        if img.shape[2] == 1:
            return False
        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        if (b == g).all() and (b == r).all():
            return False
        return True  # if not grayscale

    def openResults(self, images):

        for im in images:
            im_path = f'{os.getcwd()}/results{self.results_index}/{im}'
            icon = QIcon(im_path)

            font = QFont("Arial")
            font.setPointSize(20)

            text = ""
            if self.illness_check(im):
                text = f"  ❌ Sick\n  {im}"
            else:
                text = f"  ✅ Healthy\n  {im}"

            item = QListWidgetItem()
            item.setIcon(icon)
            item.setText(text)
            item.setFont(font)

            self.scrollResults.addItem(item)
            self.scrollResults.setIconSize(QSize(250, 250))


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        self.setFixedSize(653, 406)
        self.loadBtn.clicked.connect(self.load)
        self.homeBtn.clicked.connect(self.home)
        self.results_index = 1
        # self.settingsBtn.clicked.connect(self.settings)

    def settings(self):
        pass

    def home(self):
        print("HOME")
        ex = MyWidget()
        ex.show()

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        filenames = []
        if dialog.exec_():
            filenames = dialog.selectedFiles()
        if len(filenames) != 0:
            # TODO: check file type. If it is NIFTI, convert to PNG
            m = MainWindow(filenames=filenames, parent=self, results__dir_index=self.results_index)
            m.show()
            self.results_index += 1


try:
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
finally:
    for folder in os.listdir(os.getcwd()):
        if 'results' in folder:
            print('DELETED', folder, 'FOLDER')
            shutil.rmtree(folder)
