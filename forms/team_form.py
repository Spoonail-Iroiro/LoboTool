import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QLineEdit, QMessageBox
from PySide2.QtCore import QRect
from forms.team_form_ui import Ui_TeamForm
from controller.employee_controller import EmployeeController
from controller.abnoma_controller import AbnomaController
import  functools
from setting_const import *
from forms.select_work_abnoma_form import SelectWorkAbnomaForm
from db_accessor import *
from forms.result_form import ResultForm

class TeamForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TeamForm()
        self.ui.setupUi(self)
        self.copyEmployeeUI(self.ui)
        self.copyAbnomaUI(self.ui)
        self.selected_id_work = None

    def setup_employee_ui(self, base_set, n):

        #UIの見た目部分の設定
        copy_y_margin = 120

        copy_list = []
        # copy_list.append(base_set)
        for i in range(0,n):
            tmp = {}
            for k, v in base_set.items():
                if k.startswith("btn"):
                    v:QPushButton
                    tmp[k] = QPushButton(self)
                    tmp[k].setObjectName(k+str(i))
                if k.startswith("txt"):
                    v:QTextEdit
                    tmp[k] = QTextEdit(self)
                    tmp[k].setObjectName(k+str(i))
                if k.startswith("led"):
                    v:QLineEdit
                    tmp[k] = QLineEdit(self)
                    tmp[k].setObjectName(k+str(i))
            copy_list.append(tmp)

        # 元になったコントロールは隠す
        for k, v in base_set.items():
            v.hide()

        #Controllerを設定
        self.employee_ui_controllers = [EmployeeController(i, ui, base_set, self.get_abnoma_pri_keys) for i,ui in enumerate(copy_list)]

        #コンポーネント個別のsetupはcontrollerにやらせる
        for con in self.employee_ui_controllers:
            con.setupui()
            # 作業登録更新時のイベント登録
            con.work_registered.connect(self.work_register_updated)
            con.work_unregistered.connect(self.work_register_updated)


    def setup_abnoma_ui(self, base_set):
        copy_list = []
        for i in range(40):
            ui_set = {}
            for k, v in base_set.items():
                if k.startswith("btn"):
                    ui_set[k] = QPushButton(self)
                    ui_set[k].setObjectName(k+str(i))
                    pass
                elif k.startswith("img"):
                    ui_set[k] = QLabel(self)
                    ui_set[k].setObjectName(k+str(i))
                    # ui_set[k].setText("未設定")
                    pass
            copy_list.append(ui_set)

        self.abnoma_ui_controllers = [AbnomaController(i, ui, base_set) for i,ui in enumerate(copy_list)]

        #部門に対応するコントロールと位置ベースになるラベル位置
        dept_list = {
            "control":(self.ui.imgControl, self.abnoma_ui_controllers[0:4]),
            "info":(self.ui.imgInfo, self.abnoma_ui_controllers[4:8]),
            "train":(self.ui.imgTrain, self.abnoma_ui_controllers[8:12]),
            "safe":(self.ui.imgSafe, self.abnoma_ui_controllers[12:16]),
            "center1":(self.ui.imgCenter1, self.abnoma_ui_controllers[16:20]),
            "center2":(self.ui.imgCenter2, self.abnoma_ui_controllers[20:24]),
            "panish":(self.ui.imgPanish, self.abnoma_ui_controllers[24:28]),
            "welfare":(self.ui.imgWelfare, self.abnoma_ui_controllers[28:32]),
            "extract":(self.ui.imgExtract, self.abnoma_ui_controllers[32:36]),
            "memory":(self.ui.imgMemory, self.abnoma_ui_controllers[36:40]),
        }
        from typing import List

        #各部門の位置へ配置（位置のみ）
        for k,v in dept_list.items():
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

        for k,v in base_set.items():
            v.hide()

        for cons in self.abnoma_ui_controllers:
            #個別のuiセットアップはcontrollerで設定
            cons.setupui()

    def copyAbnomaUI(self, ui : Ui_TeamForm):
        base_set = {component.objectName():component for component in
                    [
                        ui.imgAbnoma,
                        ui.btnRegister,
                        ui.btnStar,
                        ui.imgStared,
                        ui.imgSelected
                    ]}
        self.abnoma_ui_base = base_set

        self.setup_abnoma_ui(base_set)

    def copyEmployeeUI(self, ui : Ui_TeamForm):
        base_set = {component.objectName():component for component
                    in
                    [ui.btnInstinct,
                     ui.btnInsight,
                     ui.btnAttachment,
                     ui.btnSuppression,
                     ui.ledEmployee,
                     ui.txtAbnoma,
                     ui.btnClear
                     ]}
        print(base_set)

        self.employee_ui_base = base_set

        self.setup_employee_ui(base_set, 12)

    def btnN_clicked(self,n):
        btn = self.employee_ui_list[n]["btnInstinct"]
        txt = self.employee_ui_list[n][self.ui.txtEmployee.objectName()]
        txt.setText(str(n))

    def btnAptitude_clicked(self):
        form = SelectWorkAbnomaForm()

        form.exec_()

    # 収容中のアブノーマリティのpri_keyリストを取得
    def get_abnoma_pri_keys(self):
        pri_keys = [con.pri_key for con in self.abnoma_ui_controllers if con.pri_key is not None]

        return pri_keys

    def btnSearch_clicked(self):
        self.ui.txtSearchNo.setText("Hello")

    def work_register_updated(self):
        pri_keys = [con.abnoma_pri_key for con in self.employee_ui_controllers if con.abnoma_pri_key is not None]

        for con in self.abnoma_ui_controllers:
            if con.pri_key in pri_keys:
                con.select_abnoma()
            else:
                con.unselect_abnoma()

    def validation_doubled_abnoma(self):
        check_list = []

        for con in self.employee_ui_controllers:
            if con.abnoma_pri_key is None:
                continue
            if con.abnoma_pri_key in check_list:
                return False, con.abnoma_pri_key
            else:
                check_list.append(con.abnoma_pri_key)

        return True, None

    def validation_stared_unassigned_abnoma(self):
        stared_abnoma_pri_keys = [con.pri_key for con in self.abnoma_ui_controllers if con.pri_key is not None and con.stared]
        assigned_abnoma_pri_keys = [con.abnoma_pri_key for con in self.employee_ui_controllers if con.abnoma_pri_key is not None]

        ft_list = [stared in assigned_abnoma_pri_keys for stared in stared_abnoma_pri_keys]

        return all(ft_list)



    def btnResult_clicked(self):
        isOk, dup_pri_key = self.validation_doubled_abnoma()

        if not isOk:
            msg = QMessageBox()
            msg.setText("アブノーマリティ割当てが重複しています。続行しますか？")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            ans = msg.exec_()

            if ans == QMessageBox.No:
                return

        isOk = self.validation_stared_unassigned_abnoma()

        if not isOk:
            msg = QMessageBox()
            msg.setText("Starされたアブノーマリティに作業が割当たっていません。続行しますか？")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            ans = msg.exec_()

            if ans == QMessageBox.No:
                return


        form = ResultForm()
        result_text = ""
        with sqlite3.connect(str(db_path)) as cnn:
            for con in self.abnoma_ui_controllers:
                if con.pri_key is None:
                    continue

                assigned_employee = [en_con for en_con in self.employee_ui_controllers if en_con.abnoma_pri_key == con.pri_key]

                for assigned_con in assigned_employee:
                        acc = DBAccessor(cnn)

                        name = acc.get_abnoma_name_ja(assigned_con.abnoma_pri_key)
                        work_name = inv_work_code[assigned_con.work_code]

                        result_text += f"{name}→{assigned_con.employee_name}（{work_name}）\n\n"


        # for con in self.employee_ui_controllers:
        #     if con.abnoma_pri_key is None:
        #         continue
        #
        #     with sqlite3.connect(str(db_path)) as cnn:
        #         acc = DBAccessor(cnn)
        #
        #         name = acc.get_abnoma_name_ja(con.abnoma_pri_key)
        #         work_name = inv_work_code[con.work_code]
        #
        #         result_text += f"{name}→{con.employee_name}（{work_name}）\n\n"

        form.set_text(result_text)
        form.exec_()


    #現在の収容アブノーマリティ・作業登録状態をセーブする
    def save(self):
        records_abnoma = [ SavAbnomaRecord(con.pri_key, con.stared) for con in self.abnoma_ui_controllers]
        records_employee = [SavEmployeeRecord(con.ui_set["ledEmployee"].text(), con.work_code, con.abnoma_pri_key) for con in self.employee_ui_controllers]
        with sqlite3.connect(str(db_path)) as cnn:
            acc = DBAccessor(cnn)
            acc.save_sav_abnoma(records_abnoma)
            acc.save_sav_employee(records_employee)

    def load(self):
        with sqlite3.connect(str(db_path)) as cnn:
            acc = DBAccessor(cnn)
            table_abnoma = acc.get_sav_abnormality()
            table_employee = acc.get_sav_employee()

            for record, con in zip(table_abnoma, self.abnoma_ui_controllers):
                #pri_keyが空なら登録なし
                if record["pri_key"] is None:
                    continue
                con: AbnomaController
                pri_key = record["pri_key"]
                con.register_abnoma(pri_key)
                stared = record["stared"]
                if stared > 0:
                    con.btnStar_clicked()

            for record, con in zip(table_employee, self.employee_ui_controllers):
                if record["work_code"] is None:
                    continue
                con: EmployeeController
                con.register_work(record["work_code"], record["pri_key"])
                con.ui_set["ledEmployee"].setText(record["employee_name"])



