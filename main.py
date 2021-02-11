import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PIL import Image
import shutil
import os
import torch
import requests, cv2, tqdm, torchvision, yaml, matplotlib, pandas, seaborn


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        # self.setFixedSize(1006, 807)
        self.show()
        self.loadBtn.clicked.connect(self.load)
        self.homeBtn.clicked.connect(self.home)
        # self.settingsBtn.clicked.connect(self.settings)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model=f'{os.getcwd()}/best.pt')

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

    def analyze(self, images):
        imgs = []
        for img in images:
            imgs.append(Image.open(img))
        # TODO resize image if > 256x256
        results = self.model(imgs, size=256)
        results.print()
        if not os.path.exists('results'):
            os.mkdir('results')
        results.save(save_dir='results')


app = QApplication(sys.argv)
ex = MyWidget()
# ex.show()
sys.exit(app.exec_())
