
import PyQt5 as pq
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(385, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 256, 192))
        self.listWidget.setObjectName("listWidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(290, 10, 77, 199))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bAdd = QtWidgets.QPushButton(self.widget)
        self.bAdd.setObjectName("bAdd")
        self.verticalLayout.addWidget(self.bAdd)
        self.bEdit = QtWidgets.QPushButton(self.widget)
        self.bEdit.setObjectName("bEdit")
        self.verticalLayout.addWidget(self.bEdit)
        self.bRemove = QtWidgets.QPushButton(self.widget)
        self.bRemove.setObjectName("bRemove")
        self.verticalLayout.addWidget(self.bRemove)
        self.bUp = QtWidgets.QPushButton(self.widget)
        self.bUp.setObjectName("bUp")
        self.verticalLayout.addWidget(self.bUp)
        self.bDown = QtWidgets.QPushButton(self.widget)
        self.bDown.setObjectName("bDown")
        self.verticalLayout.addWidget(self.bDown)
        self.bSort = QtWidgets.QPushButton(self.widget)
        self.bSort.setObjectName("bSort")
        self.verticalLayout.addWidget(self.bSort)
        self.bExit = QtWidgets.QPushButton(self.widget)
        self.bExit.setObjectName("bExit")
        self.verticalLayout.addWidget(self.bExit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 385, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bAdd.setText(_translate("MainWindow", "Add"))
        self.bEdit.setText(_translate("MainWindow", "Edit"))
        self.bRemove.setText(_translate("MainWindow", "Remove"))
        self.bUp.setText(_translate("MainWindow", "Up"))
        self.bDown.setText(_translate("MainWindow", "Down"))
        self.bSort.setText(_translate("MainWindow", "Sort"))
        self.bExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
