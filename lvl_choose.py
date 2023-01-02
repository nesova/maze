from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class LvlChoose(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('lvl_choose.ui', self)
        self.lvl1_btn.clicked.connect(self.open_lvl1)
        self.lvl2_btn.clicked.connect(self.open_lvl2)
        self.lvl3_btn.clicked.connect(self.open_lvl3)

    def open_lvl1(self):
        pass

    def open_lvl2(self):
        pass

    def open_lvl3(self):
        pass
