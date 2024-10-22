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
    QMessageBox, QLabel
from nii2png import convert_slice

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


class Settings(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(get_path('settings.ui'), self)
        print('settings')
        self.homeBtn.clicked.connect(self.home)

    def home(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, filenames=None, results__dir_index=None, parent=None, recent_path: str = None):
        super().__init__(parent)
        self.results_index = results__dir_index
        self.images_list = []
        self.illness_list = []
        self.saved = False
        uic.loadUi(get_path('mainPage.ui'), self)
        if recent_path is None:
            self.analyze(filenames)
            self.openResults(os.listdir(get_path(f'results{self.results_index}')))
            self.save_detected_button.clicked.connect(self.saveResults)
        else:
            self.openResults(os.listdir(recent_path), recent_path)
        self.setWindowTitle(f'Session {self.results_index}')
        self.to_csv_button.clicked.connect(self.to_csv)

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
        img = cv2.imread(image_path)
        if len(img.shape) < 3:
            return False
        if img.shape[2] == 1:
            return False
        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        if (b == g).all() and (b == r).all():
            return False
        return True  # if not grayscale

    def openResults(self, images, recent_path=None):
        self.images_list = images

        if os.path.exists(get_path('nii')):
            shutil.rmtree(get_path('nii'))

        if recent_path is not None:
            path = recent_path
            self.saved = True
        else:
            path = os.path.join(get_path(), f'results{self.results_index}')

        for im in images:
            im_path = os.path.join(path, im)
            icon = QIcon(im_path)

            font = QFont("Arial")
            font.setPointSize(20)

            text = ""
            if self.illness_check(im_path):
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
            f = open(get_path('cache.txt'), 'w')
            f.write(new_path)
            f.close()
            self.saved = True

    def closeEvent(self, event):
        if not self.saved:
            reply = QMessageBox.question(self, 'Session End', 'You have unsaved detected images! \nDo you want to save '
                                                              'them?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

            if reply == QMessageBox.No:
                event.accept()
            elif reply == QMessageBox.Yes:
                self.saveResults()
                event.accept()
                print(f'Session{self.results_index} closed')
            else:
                event.ignore()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_path('covid.ui'), self)
        self.settingsBtn.clicked.connect(self.settings)
        self.loadBtn.clicked.connect(self.load)
        self.homeBtn.clicked.connect(self.home)
        self.recentBtn.clicked.connect(self.recent)
        self.results_index = 1
        # self.settingsBtn.clicked.connect(self.settings)

    def settings(self):
        settings = Settings(parent=self)
        settings.show()

    def home(self):
        print("HOME")
        ex = MyWidget()
        ex.show()

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        filenames = []
        nii_filenames = []
        files = []
        if dialog.exec_():
            files = dialog.selectedFiles()
        if len(files) != 0:
            # TODO: check file type. If it is NIFTI, convert to PNG
            for file in files:
                if os.path.splitext(file)[1] == '.nii':
                    convert_slice(file, 'nii', 20)
                else:
                    filenames.append(file)
            if os.path.exists(os.path.join(get_path(), 'nii')):
                for file in os.listdir(os.path.join(get_path(), 'nii')):
                    nii_filenames.append(os.path.join(get_path(), 'nii', file))
            print(filenames)
            print(nii_filenames)
            m = MainWindow(filenames=filenames + nii_filenames, parent=self, results__dir_index=self.results_index)
            m.show()
            self.results_index += 1

    def recent(self):
        recent_path = None
        if not os.path.exists(get_path('cache.txt')):
            alert = QMessageBox()
            alert.setText("You haven't saved any images yet.")
            alert.exec_()
        else:
            f = open(get_path('cache.txt'), 'r')
            recent_path = f.read()
            f.close()
            if not os.path.exists(recent_path):
                alert = QMessageBox()
                alert.setText(f"Nothing found at:\n\n{recent_path}\n\nImages may be moved or deleted.")
                alert.exec_()
            else:
                m = MainWindow(parent=self, results__dir_index=self.results_index, recent_path=recent_path)
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
