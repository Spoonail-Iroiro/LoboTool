# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './forms/result_form.ui'
#
# Created: Sun Oct 14 23:01:11 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ResultForm(object):
    def setupUi(self, ResultForm):
        ResultForm.setObjectName("ResultForm")
        ResultForm.resize(732, 861)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        ResultForm.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(ResultForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtMain = QtWidgets.QPlainTextEdit(ResultForm)
        self.txtMain.setObjectName("txtMain")
        self.verticalLayout.addWidget(self.txtMain)

        self.retranslateUi(ResultForm)
        QtCore.QMetaObject.connectSlotsByName(ResultForm)

    def retranslateUi(self, ResultForm):
        ResultForm.setWindowTitle(QtWidgets.QApplication.translate("ResultForm", "Dialog", None, -1))

