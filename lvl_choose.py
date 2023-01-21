from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from main import start_game
from PyQt5 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class LvlChoose(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('lvl_choose.ui', self)
        self.lvl1_btn.clicked.connect(self.open_lvl1)
        self.lvl2_btn.clicked.connect(self.open_lvl2)
        self.lvl3_btn.clicked.connect(self.open_lvl3)

    def open_lvl1(self):
        self.hide()
        if start_game(0):
            self.show()

    def open_lvl2(self):
        self.hide()
        if start_game(1):
            self.show()

    def open_lvl3(self):
        pass
