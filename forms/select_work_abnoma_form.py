import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QWidget, QDialog
import setting_const as setting
from custom_component.dgv_table_model import *
import sqlite3
from pathlib import  Path
from PySide2.QtWidgets import QHeaderView
from my_qt_util import *

from forms.select_work_abnoma_form_ui import Ui_SelectWorkAbnomaForm
from forms.set_work_apetitude_form import SetWorkApetitudeForm

class SelectWorkAbnomaForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SelectWorkAbnomaForm()
        self.ui.setupUi(self)

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
        mdl.add_column(DGVColumn("inst_code", "本能"))
        mdl.add_column(DGVColumn("insi_code", "洞察"))
        mdl.add_column(DGVColumn("atta_code", "愛着"))
        mdl.add_column(DGVColumn("supr_code", "抑圧"))
        self.table_model = mdl

        #モデルをViewにセット
        self.ui.tvMain.setModel(self.table_model)

    def btnEdit_clicked(self):
        row = get_selected_table_row(self.ui.tvMain, self.table_model.get_datasource())
        if row is None:
            return

        pri_key = row["pri_key"]

        form = SetWorkApetitudeForm(pri_key)
        form.exec_()

        self.reload_table()
        pass

    def btnCancel_clicked(self):
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
                FROM v_abnormality_info
                {}
                UNION
                SELECT *
                FROM v_abnormality_info
                {}
                """
            select_sql = select_sql.format(where_phrase_en, where_phrase_ja)
            table = [*cnn.execute(select_sql)]

            self.table_model.bind_datasource(table)

