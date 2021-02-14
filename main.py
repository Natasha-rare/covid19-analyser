import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QLabel
from PIL import Image
import shutil
import os
import torch
import requests, cv2, tqdm, torchvision, yaml, matplotlib, pandas, seaborn


class CreateMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainPage.ui', self)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        # self.setFixedSize(1006, 807)
        self.show()
        self.loadBtn.clicked.connect(self.load)
        self.homeBtn.clicked.connect(self.home)
        # self.settingsBtn.clicked.connect(self.settings)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path_or_model=f'{os.getcwd()}/best.pt')

    def home(self):
        uic.loadUi('covid.ui', self)

    def settings(self):
        pass

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        filenames = []
        if dialog.exec_():
            filenames = dialog.selectedFiles()
        # TODO: check file type. If it is NIFTI, convert to PNG
        self.analyze(filenames)
        self.openResults(filenames)

    def analyze(self, filenames):
        images = []
        for img in filenames:
            images.append(Image.open(img))
        results = self.model(images, size=256)
        results.print()
        if not os.path.exists('results'):
            os.mkdir('results')
        results.save()

    def illness_check(self, image_path):
        img = cv2.imread(image_path)
        if len(img.shape) < 3:
            return False
        if img.shape[2] == 1:
            return False
        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        if (b == g).all() and (b == r).all():
            return False
        return True  # if not grayscale

    def openResults(self, images):
        main = uic.loadUi('mainPage.ui', self)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        main.show()
        print('opened')
        # self.close()

        for im in images:
            imageLabel = QLabel()
            imageLabel.setPixmap(QPixmap.fromImage(QImage(im)))
            is_ill = self.illness_check(im)
            main.srollResults.setWidget(imageLabel)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
