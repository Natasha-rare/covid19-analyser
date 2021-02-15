import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QLabel, QListWidget, QListWidgetItem
from PIL import Image
import shutil
import os
import torch
import requests, cv2, tqdm, torchvision, yaml, matplotlib, pandas, seaborn

class SessionWindow(QMainWindow):
    def __init__(self, filenames):
        super().__init__()
        uic.loadUi('mainPage.ui', self)
        self.show()
        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path_or_model=f'{os.getcwd()}/best.pt')
        self.analyze(filenames)
        self.openResults(os.listdir('results'))
        self.homeBtn.clicked.connect(self.home)

    def home(self):
        print('HOME')
        covid = uic.loadUi('covid.ui', self)
        covid.show()

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
        img = cv2.imread(f'{os.getcwd()}/results/{image_path}')
        if len(img.shape) < 3:
            return False
        if img.shape[2] == 1:
            return False
        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        if (b == g).all() and (b == r).all():
            return False
        return True  # if not grayscale

    def openResults(self, images):
        print('PASSED IMAGES', images)
        for im in images:
            im_path = f'{os.getcwd()}/results/{im}'
            icon = QIcon(im_path)
            text = ""
            if self.illness_check(im):
                text = "Is ill"
            else:
                text = "is not ill"
            item = QListWidgetItem(icon, text)
            self.srollResults.addItem(item)
