# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './forms/select_abnoma_form.ui'
#
# Created: Sun Oct 14 12:13:30 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectAbnomaForm(object):
    def setupUi(self, SelectAbnomaForm):
        SelectAbnomaForm.setObjectName("SelectAbnomaForm")
        SelectAbnomaForm.resize(364, 465)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectAbnomaForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtSearch = QtWidgets.QLineEdit(SelectAbnomaForm)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.txtSearch.setFont(font)
        self.txtSearch.setObjectName("txtSearch")
        self.verticalLayout.addWidget(self.txtSearch)
        self.tvMain = QtWidgets.QTableView(SelectAbnomaForm)
        self.tvMain.setObjectName("tvMain")
        self.verticalLayout.addWidget(self.tvMain)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnCancel = QtWidgets.QPushButton(SelectAbnomaForm)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.btnCancel.setFont(font)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnReset = QtWidgets.QPushButton(SelectAbnomaForm)
        self.btnReset.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.btnReset.setFont(font)
        self.btnReset.setObjectName("btnReset")
        self.horizontalLayout.addWidget(self.btnReset)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnOK = QtWidgets.QPushButton(SelectAbnomaForm)
        self.btnOK.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.btnOK.setFont(font)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout.addWidget(self.btnOK)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(SelectAbnomaForm)
        QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL("clicked()"), SelectAbnomaForm.btnOK_clicked)
        QtCore.QObject.connect(self.btnReset, QtCore.SIGNAL("clicked()"), SelectAbnomaForm.btnReset_clicked)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), SelectAbnomaForm.btnCancel_clicked)
        QtCore.QObject.connect(self.txtSearch, QtCore.SIGNAL("textChanged(QString)"), SelectAbnomaForm.txtSearch_textChanged)
        QtCore.QMetaObject.connectSlotsByName(SelectAbnomaForm)

    def retranslateUi(self, SelectAbnomaForm):
        SelectAbnomaForm.setWindowTitle(QtWidgets.QApplication.translate("SelectAbnomaForm", "Dialog", None, -1))
        self.btnCancel.setText(QtWidgets.QApplication.translate("SelectAbnomaForm", "戻る", None, -1))
        self.btnReset.setText(QtWidgets.QApplication.translate("SelectAbnomaForm", "登録解除", None, -1))
        self.btnOK.setText(QtWidgets.QApplication.translate("SelectAbnomaForm", "OK", None, -1))

