
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QApplication
from MacrosUI import Ui_MainWindow
import sys
import pyautogui as pag
from pynput import keyboard

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def keyPressEvent(self, e):
        print(e.text())


def app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

app()