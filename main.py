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


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('covid.ui', self)
        # self.setFixedSize(1006, 807)
        self.loadBtn.clicked.connect(self.load)
        self.homeBtn.clicked.connect(self.home)
        # self.settingsBtn.clicked.connect(self.settings)

    def home(self):
        print("HOME CLICKED")
        self.close()
        uic.loadUi('covid.ui', self)
        widget = MyWidget()
        widget.show()
        self.show()

    def settings(self):
        pass

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        filenames = []
        if dialog.exec_():
            filenames = dialog.selectedFiles()
        if len(filenames) != 0:
            # TODO: check file type. If it is NIFTI, convert to PNG
            self.analyze(filenames)
            self.openResults(os.listdir('results'))

    def analyze(self, filenames):
        print('LOADING MODEL:')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path_or_model=f'{os.getcwd()}/best.pt')
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
        main = uic.loadUi('mainPage.ui', self)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        main.homeButton.clicked.connect(self.home)
        main.endBtn.clicked.connect(self.home)
        main.show()

        for im in images:
            im_path = f'{os.getcwd()}/results/{im}'
            icon = QIcon(im_path)

            font = QFont("Georgia")
            font.bold()
            font.setPointSize(30)

            text = ""
            if self.illness_check(im):
                text = "❌ Sick"
            else:
                text = "✅ Healthy"

            item = QListWidgetItem()
            item.setIcon(icon)
            item.setText(text)
            item.setFont(font)

            main.scrollResults.addItem(item)
            main.scrollResults.setIconSize(QSize(200, 200))


try:
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
finally:
    if os.path.exists('results'):
        shutil.rmtree('results')
