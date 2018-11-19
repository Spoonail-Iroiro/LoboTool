import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QWidget, \
    QDialog
from PySide2.QtWidgets import QHeaderView
from PySide2.QtCore import QRect
from forms.select_target_form_ui import Ui_SelectTargetForm
from controller.employee_controller import EmployeeController
import functools
from setting_const import *
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QWidget, \
    QDialog
from custom_component.dgv_table_model import *
import sqlite3
from pathlib import Path
from PySide2.QtWidgets import QHeaderView
from my_qt_util import *
from db_accessor import DBAccessor


class SelectTargetForm(QDialog):
    # 作業種類と、収容中のアブノーマリティのpri_keyを受け取る
    def __init__(self, work_code, pri_keys):
        super().__init__()
        self.ui = Ui_SelectTargetForm()
        self.ui.setupUi(self)
        self.work_code = work_code
        self.pri_keys = pri_keys
        self.result_pri_key = None

        # カラム幅がコンテンツにフィットするように
        header: QHeaderView = self.ui.tvMain.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader: QHeaderView = self.ui.tvMain.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader.hide()

        # 選択モードはDesignerで設定済み

        mdl = DGVTableModel()

        mdl.add_column(DGVColumn("no", "No."))
        mdl.add_column(AbnomaThumbnailColumn("name_key", ""))
        mdl.add_column(DGVColumn("name_ja", "名前"))
        self.table_model = mdl

        # モデルをViewにセット
        self.ui.tvMain.setModel(self.table_model)

        self.reload_table()

    def chkUpper100_stateChanged(self, num):
        self.reload_table()

    def reload_table(self):
        with sqlite3.connect(str(db_path)) as cnn:
            acc = DBAccessor(cnn)

            #100以上にチェックが付いていれば100以上適性『も』表示する
            app_codes = ["01"] if not self.ui.chkUpper100.isChecked() else ["01","02"]

            table = acc.get_target_abnoma(self.work_code, app_codes, self.pri_keys)

            self.table_model.bind_datasource(table)


    def btnOK_clicked(self):

        row = get_selected_table_row(self.ui.tvMain, self.table_model.get_datasource())

        if row is not None:
            self.result_pri_key = row["pri_key"]

        self.close()
