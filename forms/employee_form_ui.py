# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './forms/employee_form.ui'
#
# Created: Mon Nov 19 14:48:34 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_EmployeeForm(object):
    def setupUi(self, EmployeeForm):
        EmployeeForm.setObjectName("EmployeeForm")
        EmployeeForm.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        EmployeeForm.setFont(font)
        self.btnSuppression = QtWidgets.QPushButton(EmployeeForm)
        self.btnSuppression.setGeometry(QtCore.QRect(60, 90, 41, 41))
        self.btnSuppression.setObjectName("btnSuppression")
        self.btnInstinct = QtWidgets.QPushButton(EmployeeForm)
        self.btnInstinct.setGeometry(QtCore.QRect(20, 50, 41, 41))
        self.btnInstinct.setObjectName("btnInstinct")
        self.btnInsight = QtWidgets.QPushButton(EmployeeForm)
        self.btnInsight.setGeometry(QtCore.QRect(60, 50, 41, 41))
        self.btnInsight.setObjectName("btnInsight")
        self.btnAttachment = QtWidgets.QPushButton(EmployeeForm)
        self.btnAttachment.setGeometry(QtCore.QRect(20, 90, 41, 41))
        self.btnAttachment.setObjectName("btnAttachment")
        self.ledEmployee = QtWidgets.QLineEdit(EmployeeForm)
        self.ledEmployee.setGeometry(QtCore.QRect(20, 20, 241, 31))
        self.ledEmployee.setObjectName("ledEmployee")
        self.txtAbnoma = QtWidgets.QPlainTextEdit(EmployeeForm)
        self.txtAbnoma.setGeometry(QtCore.QRect(100, 50, 271, 51))
        self.txtAbnoma.setObjectName("txtAbnoma")
        self.btnClear = QtWidgets.QPushButton(EmployeeForm)
        self.btnClear.setGeometry(QtCore.QRect(260, 20, 111, 31))
        self.btnClear.setObjectName("btnClear")

        self.retranslateUi(EmployeeForm)
        QtCore.QMetaObject.connectSlotsByName(EmployeeForm)

    def retranslateUi(self, EmployeeForm):
        EmployeeForm.setWindowTitle(QtWidgets.QApplication.translate("EmployeeForm", "Dialog", None, -1))
        self.btnSuppression.setText(QtWidgets.QApplication.translate("EmployeeForm", "抑圧", None, -1))
        self.btnInstinct.setText(QtWidgets.QApplication.translate("EmployeeForm", "本能", None, -1))
        self.btnInsight.setText(QtWidgets.QApplication.translate("EmployeeForm", "洞察", None, -1))
        self.btnAttachment.setText(QtWidgets.QApplication.translate("EmployeeForm", "愛着", None, -1))
        self.btnClear.setText(QtWidgets.QApplication.translate("EmployeeForm", "削除", None, -1))

