# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogBox1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Input(object):
    def setupUi(self, Input):
        Input.setObjectName("Input")
        Input.resize(400, 93)
        self.label = QtWidgets.QLabel(Input)
        self.label.setGeometry(QtCore.QRect(20, 20, 341, 41))
        self.label.setObjectName("label")

        self.retranslateUi(Input)
        QtCore.QMetaObject.connectSlotsByName(Input)

    def retranslateUi(self, Input):
        _translate = QtCore.QCoreApplication.translate
        Input.setWindowTitle(_translate("Input", "Dialog"))
        self.label.setText(_translate("Input", "Press the key you want to add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Input = QtWidgets.QDialog()
    ui = Ui_Input()
    ui.setupUi(Input)
    Input.show()
    sys.exit(app.exec_())