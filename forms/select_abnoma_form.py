import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QWidget, QDialog
from forms.select_abnoma_form_ui import Ui_SelectAbnomaForm
import setting_const as setting
from custom_component.dgv_table_model import *
import sqlite3
from pathlib import  Path
from PySide2.QtWidgets import QHeaderView
from my_qt_util import *


class SelectAbnomaForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SelectAbnomaForm()
        self.ui.setupUi(self)
        self.table = None

        self.result_pri_key = None
        self.result_is_reset = False

        #カラム幅がコンテンツにフィットするように
        header: QHeaderView = self.ui.tvMain.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader: QHeaderView = self.ui.tvMain.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader.hide()

        #選択は行、1つのみ
        from PySide2.QtWidgets import QAbstractItemView
        self.ui.tvMain.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tvMain.setSelectionMode(QAbstractItemView.SingleSelection)

        #Modelの用意
        mdl = DGVTableModel()
        mdl.add_column(DGVColumn("no", "No."))
        mdl.add_column(AbnomaThumbnailColumn("name_key", ""))
        mdl.add_column(DGVColumn("name_ja", "名前"))
        mdl.add_column(DGVColumn("risk_level", "リスクレベル", format_func=lambda str_: setting.inv_risk_level_code[str_]))
        self.table_model = mdl

        #モデルをViewにセット
        self.ui.tvMain.setModel(self.table_model)

    def btnOK_clicked(self):
        row = get_selected_table_row(self.ui.tvMain, self.table_model.get_datasource())

        if row is None:
            self.result_pri_key = None
        else:
            self.result_pri_key = row["pri_key"]

        self.close()

    def btnCancel_clicked(self):
        self.close()

    def btnReset_clicked(self):
        self.result_is_reset = True
        self.close()

    def txtSearch_textChanged(self):
        self.reload_table()


    def reload_table(self):
        search_word = self.ui.txtSearch.text()
        where_phrase_en = f"WHERE name_en LIKE '%{search_word}%'"
        where_phrase_ja = f"WHERE name_ja LIKE '%{search_word}%'"
        with sqlite3.connect(str(setting.db_path)) as cnn:
            cnn.row_factory = sqlite3.Row
            select_sql ="""
                SELECT *
                FROM m_abnormality
                {}
                UNION
                SELECT *
                FROM m_abnormality
                {}
                """
            select_sql = select_sql.format(where_phrase_en, where_phrase_ja)
            table = [*cnn.execute(select_sql)]

            self.table_model.bind_datasource(table)

