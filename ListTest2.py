
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QApplication
from ListTest import Ui_MainWindow
import sys

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.bAdd.clicked.connect(self.addCommand)
    
    def addCommand(self):
        currentIndex = self.ui.listWidget.currentRow()
        text, ok = QInputDialog.getText(self, 'blah', 'another blah')
        if ok and text is not None:
            self.ui.listWidget.insertItem(currentIndex +1, text)


def app():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

app()