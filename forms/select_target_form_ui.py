# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './forms/select_target_form.ui'
#
# Created: Sun Oct 14 23:01:06 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectTargetForm(object):
    def setupUi(self, SelectTargetForm):
        SelectTargetForm.setObjectName("SelectTargetForm")
        SelectTargetForm.resize(411, 416)
        self.chkUpper100 = QtWidgets.QCheckBox(SelectTargetForm)
        self.chkUpper100.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.chkUpper100.setObjectName("chkUpper100")
        self.btnOK = QtWidgets.QPushButton(SelectTargetForm)
        self.btnOK.setGeometry(QtCore.QRect(310, 370, 93, 41))
        self.btnOK.setObjectName("btnOK")
        self.tvMain = QtWidgets.QTableView(SelectTargetForm)
        self.tvMain.setGeometry(QtCore.QRect(100, 10, 301, 351))
        self.tvMain.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tvMain.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tvMain.setObjectName("tvMain")

        self.retranslateUi(SelectTargetForm)
        QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL("clicked()"), SelectTargetForm.btnOK_clicked)
        QtCore.QObject.connect(self.chkUpper100, QtCore.SIGNAL("stateChanged(int)"), SelectTargetForm.chkUpper100_stateChanged)
        QtCore.QMetaObject.connectSlotsByName(SelectTargetForm)

    def retranslateUi(self, SelectTargetForm):
        SelectTargetForm.setWindowTitle(QtWidgets.QApplication.translate("SelectTargetForm", "Form", None, -1))
        self.chkUpper100.setText(QtWidgets.QApplication.translate("SelectTargetForm", "100以上", None, -1))
        self.btnOK.setText(QtWidgets.QApplication.translate("SelectTargetForm", "OK", None, -1))

