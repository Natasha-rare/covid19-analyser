import os
import shutil
import sys

import PyQt5
import cv2
import pandas as pd
import torch
from PIL import Image
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, \
    QMessageBox

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# if not getattr(sys, 'frozen', False):
#     application_path = os.path.dirname(os.path.abspath(__file__))
# else:
#     # If the application is run as a bundle, the PyInstaller bootloader
#     # extends the sys module by a flag frozen=True and sets the app
#     # path into variable _MEIPASS'.
#     application_path = sys._MEIPASS
application_path = os.path.dirname(os.path.abspath(__file__))


def get_path(file=None):
    if file is not None:
        return os.path.join(application_path, file)
    return application_path


class MainWindow(QMainWindow):
    def __init__(self, filenames=None, results__dir_index=None, parent=None):
        super().__init__(parent)
        self.results_index = results__dir_index
        self.images_list = []
        self.illness_list = []
        self.saved = False
        uic.loadUi(get_path('mainPage.ui'), self)
        self.analyze(filenames)
        self.openResults(os.listdir(get_path(f'results{self.results_index}')))
        self.setWindowTitle(f'Session {self.results_index}')
        self.to_csv_button.clicked.connect(self.to_csv)
        self.save_detected_button.clicked.connect(self.saveResults)

    def analyze(self, filenames):
        print('LOADING MODEL:')
        # NOTE! If model does not work, try this (Windows ONLY!!!!!)
        # {your python.exe path} -m pip install torch==1.7.1+cpu
        # torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path_or_model=get_path('best.pt'))
        images = []
        for img in filenames:
            images.append(Image.open(img))
        results = self.model(images, size=256)
        results.print()
        if not os.path.exists(get_path(f'results{self.results_index}')):
            os.mkdir(get_path(f'results{self.results_index}'))
        results.save(get_path(f'results{self.results_index}'))

    def illness_check(self, image_path):
        img = cv2.imread(f'{get_path()}/results{self.results_index}/{image_path}')
        if len(img.shape) < 3:
            return False
        if img.shape[2] == 1:
            return False
        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        if (b == g).all() and (b == r).all():
            return False
        return True  # if not grayscale

    def openResults(self, images):
        self.images_list = images
        for im in images:
            im_path = f'{get_path()}/results{self.results_index}/{im}'
            icon = QIcon(im_path)

            font = QFont("Arial")
            font.setPointSize(20)

            text = ""
            if self.illness_check(im):
                text = f"  ❌ Sick\n  {im}"
                self.illness_list.append(1)
            else:
                text = f"  ✅ Healthy\n  {im}"
                self.illness_list.append(0)

            item = QListWidgetItem()
            item.setIcon(icon)
            item.setText(text)
            item.setFont(font)

            self.scrollResults.addItem(item)
            self.scrollResults.setIconSize(QSize(250, 250))

    def to_csv(self):
        df = pd.DataFrame(list(zip(self.images_list, self.illness_list)),
                          columns=['File', 'Covid'])
        # TODO: test saving on Windows
        name = QFileDialog.getSaveFileName(self, caption='Save session as .csv',
                                           directory=f'{os.path.expanduser("~/Desktop")}/session{self.results_index}.csv',
                                           filter='*.csv')
        if name[0] != '':
            df.to_csv(name[0])

    def saveResults(self):
        dir_name = QFileDialog.getExistingDirectory(self, caption='Choose folder',
                                                    directory=f'{os.path.expanduser("~/Desktop")}',
                                                    options=QFileDialog.ShowDirsOnly)
        if dir_name != "":
            orig_path = f'{get_path()}/results{self.results_index}'
            new_path = f'{dir_name}/results{self.results_index}'
            shutil.move(orig_path, new_path)
            self.saved = True

    def closeEvent(self, event):
        if not self.saved:
            reply = QMessageBox.question(self, 'Session End', 'You have unsaved detected images! \nDo you want to save '
                                                              'them?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.No:
                event.accept()
            else:
                self.saveResults()
                event.accept()
            print(f'Session{self.results_index} closed')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_path('covid.ui'), self)

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
    for folder in os.listdir(get_path()):
        if 'results' in folder:
            shutil.rmtree(get_path(folder))
            print('DELETED', folder, 'FOLDER')
