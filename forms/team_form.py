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
from controller.employees_manager import EmployeesManger
from controller.abnomas_manager import AbnomasManager
from forms.employee_form import EmployeeForm

class TeamForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TeamForm()
        self.ui.setupUi(self)
        self.hide_EmployeeUI(self.ui)
        self.employee_form = EmployeeForm()
        #エージェント登録窓が作成したemployees_managerをもらう
        self.employees_manager = self.employee_form.employees_manager
        # self.copyEmployeeUI(self.ui)
        self.copyAbnomaUI(self.ui)
        self.selected_id_work = None

    def showEvent(self, *args, **kwargs):
        # self.employee_form = EmployeeForm(self.get_abnoma_pri_keys)
        self.employee_form.show()

    def closeEvent(self, *args, **kwargs):
        self.employee_form.close()

    #エージェント登録ウィンドウ分離前のUIを隠す
    def hide_EmployeeUI(self, ui : Ui_TeamForm):
        base_set = [ui.btnInstinct,
                     ui.btnInsight,
                     ui.btnAttachment,
                     ui.btnSuppression,
                     ui.ledEmployee,
                     ui.txtAbnoma,
                     ui.btnClear
                     ]
        for ui1 in base_set:
            ui1.hide()

        ui.btnResult.hide()


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
        self.employee_ui_base = base_set

        self.setup_employee_ui(base_set, 12)

    def setup_employee_ui(self, base_set, n):

        #フォーム上のコントローラをコピーしてemployees_managerに渡す
        #UIのセットアップなどはmanagerにおまかせ
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
        employee_ui_controllers = [EmployeeController(i, ui, base_set) for i,ui in enumerate(copy_list)]
        self.employees_manager = EmployeesManger()
        # _ = map(self.employees_manager.add_controller, employee_ui_controllers)
        for con in employee_ui_controllers:
            self.employees_manager.add_controller(con)

        #uiセットアップ
        self.employees_manager.setupui()

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

        abnoma_ui_controllers = [AbnomaController(i, ui, base_set) for i,ui in enumerate(copy_list)]
        self.abnomas_manager = AbnomasManager()
        self.employees_manager.connect_AbnomasManager(self.abnomas_manager)
        # map(self.abnomas_manager.add_controller, abnoma_ui_controllers)
        for con in abnoma_ui_controllers:
            self.abnomas_manager.add_controller(con)

        #部門に対応するコントロールと位置ベースになるラベル位置
        dept_list = {
            "control":(self.ui.imgControl, abnoma_ui_controllers[0:4]),
            "info":(self.ui.imgInfo, abnoma_ui_controllers[4:8]),
            "train":(self.ui.imgTrain, abnoma_ui_controllers[8:12]),
            "safe":(self.ui.imgSafe, abnoma_ui_controllers[12:16]),
            "center1":(self.ui.imgCenter1, abnoma_ui_controllers[16:20]),
            "center2":(self.ui.imgCenter2, abnoma_ui_controllers[20:24]),
            "panish":(self.ui.imgPanish, abnoma_ui_controllers[24:28]),
            "welfare":(self.ui.imgWelfare, abnoma_ui_controllers[28:32]),
            "extract":(self.ui.imgExtract, abnoma_ui_controllers[32:36]),
            "memory":(self.ui.imgMemory, abnoma_ui_controllers[36:40]),
        }

        self.abnomas_manager.set_dept_list(dept_list)

        self.abnomas_manager.setupui()

        for k,v in base_set.items():
            v.hide()

    def btnAptitude_clicked(self):
        form = SelectWorkAbnomaForm()

        form.exec_()


    def load(self):
        self.employees_manager.load()

    def save(self):
        self.employees_manager.save()

    def btnSearch_clicked(self):
        pass






