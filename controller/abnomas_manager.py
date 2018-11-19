from db_accessor import DBAccessor, SavAbnomaRecord, SavEmployeeRecord
from controller.abnoma_controller import AbnomaController
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QLineEdit, QMessageBox
from PySide2.QtCore import QRect
from typing import List

class AbnomasManager():
    def __init__(self):
        self._controllers = []
        self._dept_list = {}

    def add_controller(self, controller):
        controller.set_parent_manager(self)
        self._controllers.append(controller)

    def set_dept_list(self, dept_list):
        self._dept_list = dept_list

    def setupui(self):
        #各部門の位置へ配置（位置のみ）
        for k,v in self._dept_list.items():
            base_obj : QLabel = v[0]
            base_loc = base_obj.geometry()
            target_cons : List[AbnomaController] = v[1]
            for i, con in enumerate(target_cons):
                rect = QRect(base_loc)
                rect.moveLeft(rect.left() + rect.width() * i)
                for k in con.ui_set.keys():
                    img_ui = con.ui_set[k]
                    img_ui.setGeometry(rect)

            base_obj.hide()


        for cons in self._controllers:
            #個別のuiセットアップはcontrollerで設定
            cons.setupui()


    def update_abnoma_select(self, pri_keys):
        for con in self._controllers:
            if con.pri_key in pri_keys:
                con.select_abnoma()
            else:
                con.unselect_abnoma()

    def get_abnoma_pri_keys(self):
        pri_keys = [con.pri_key for con in self._controllers if con.pri_key is not None]

        return pri_keys

    def get_stared_abnoma_pri_keys(self):
        stared_abnoma_pri_keys = [con.pri_key for con in self._controllers if con.pri_key is not None and con.stared]
        return stared_abnoma_pri_keys

    def get_assigned_abnoma_pri_keys(self):
        # assigned_abnoma_pri_keys = [con.pri_key for con in self._controllers if con.pri_key is not None]
        return self.get_abnoma_pri_keys()

    def get_sav_abnoma_records(self):
        records_abnoma = [ SavAbnomaRecord(con.pri_key, con.stared) for con in self._controllers]

        return records_abnoma

    def load(self, table_abnoma):
        for record, con in zip(table_abnoma, self._controllers):
            #pri_keyが空なら登録なし
            if record["pri_key"] is None:
                continue
            con: AbnomaController
            pri_key = record["pri_key"]
            con.register_abnoma(pri_key)
            stared = record["stared"]
            if stared > 0:
                con.btnStar_clicked()



