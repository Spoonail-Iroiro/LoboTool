from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QWidget, QDialog
from setting_const import *
import sqlite3
from db_accessor import DBAccessor
from pathlib import  Path
from PySide2.QtWidgets import QHeaderView
from forms.set_work_apetitude_form_ui import Ui_SetWorkApetitudeForm

class SetWorkApetitudeForm(QDialog):
    def __init__(self, abnoma_pri_key):
        super().__init__()
        self.ui = Ui_SetWorkApetitudeForm()
        self.ui.setupUi(self)
        self.pri_key = abnoma_pri_key

        saved_app = None

        with sqlite3.connect(str(db_path)) as cnn:
            acc = DBAccessor(cnn)
            self.ui.lblAbnormality.setText(acc.get_abnoma_name_ja(self.pri_key))
            saved_app = acc.get_abnoma_work_appetitude(self.pri_key)

        self.cmbs = [
            self.ui.cmbInst,
            self.ui.cmbInsi,
            self.ui.cmbAtta,
            self.ui.cmbSupr
        ]

        for cmb in self.cmbs:
            for k, v in appetitude_code.items():
                cmb.addItem(k, v)

        for i, cmb in enumerate(self.cmbs):
            app = saved_app[i]
            idx = cmb.findData(app)
            if idx < 0:
                continue
            else:
                cmb.setCurrentIndex(idx)


    def btnOK_clicked(self):
        cmb = self.cmbs[0]

        app_codes = [cmb.itemData(cmb.currentIndex()) for cmb in self.cmbs]

        with sqlite3.connect(str(db_path)) as cnn:
            acc = DBAccessor(cnn)

            result = acc.update_abnoma_work_appetitude(self.pri_key, *app_codes)

        self.close()





