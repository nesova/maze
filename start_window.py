import sys
from lvl_choose import LvlChoose
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('start_window.ui', self)
        self.start_btn.clicked.connect(self.open_lvl_choose)

    def open_lvl_choose(self):
        self.lvl_choose = LvlChoose()
        self.close()
        self.lvl_choose.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = StartWindow()
    sw.show()
    sys.exit(app.exec_())
