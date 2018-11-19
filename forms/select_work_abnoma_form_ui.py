# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './forms/select_work_abnoma_form.ui'
#
# Created: Sun Oct 14 12:18:22 2018
#      by: pyside2-uic 2.0.0 running on PySide2 5.6.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectWorkAbnomaForm(object):
    def setupUi(self, SelectWorkAbnomaForm):
        SelectWorkAbnomaForm.setObjectName("SelectWorkAbnomaForm")
        SelectWorkAbnomaForm.resize(364, 465)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectWorkAbnomaForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtSearch = QtWidgets.QLineEdit(SelectWorkAbnomaForm)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.txtSearch.setFont(font)
        self.txtSearch.setObjectName("txtSearch")
        self.verticalLayout.addWidget(self.txtSearch)
        self.tvMain = QtWidgets.QTableView(SelectWorkAbnomaForm)
        self.tvMain.setObjectName("tvMain")
        self.verticalLayout.addWidget(self.tvMain)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnCancel = QtWidgets.QPushButton(SelectWorkAbnomaForm)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.btnCancel.setFont(font)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnOK = QtWidgets.QPushButton(SelectWorkAbnomaForm)
        self.btnOK.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.btnOK.setFont(font)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout.addWidget(self.btnOK)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(SelectWorkAbnomaForm)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), SelectWorkAbnomaForm.btnCancel_clicked)
        QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL("clicked()"), SelectWorkAbnomaForm.btnEdit_clicked)
        QtCore.QObject.connect(self.txtSearch, QtCore.SIGNAL("textChanged(QString)"), SelectWorkAbnomaForm.txtSearch_textChanged)
        QtCore.QMetaObject.connectSlotsByName(SelectWorkAbnomaForm)

    def retranslateUi(self, SelectWorkAbnomaForm):
        SelectWorkAbnomaForm.setWindowTitle(QtWidgets.QApplication.translate("SelectWorkAbnomaForm", "Dialog", None, -1))
        self.btnCancel.setText(QtWidgets.QApplication.translate("SelectWorkAbnomaForm", "戻る", None, -1))
        self.btnOK.setText(QtWidgets.QApplication.translate("SelectWorkAbnomaForm", "編集", None, -1))

