from PySide2.QtWidgets import QDialog, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QLineEdit, QMessageBox
from PySide2.QtCore import QRect, Qt
from forms.employee_form_ui import Ui_EmployeeForm
from controller.employee_controller import EmployeeController
from controller.abnoma_controller import AbnomaController
import  functools
from forms.select_work_abnoma_form import SelectWorkAbnomaForm
from forms.result_form import ResultForm
from controller.employees_manager import EmployeesManger

class EmployeeForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EmployeeForm()
        self.setWindowFlags(Qt.Window |
                            Qt.CustomizeWindowHint |
                            Qt.WindowTitleHint |
                            Qt.WindowMinimizeButtonHint)
        self.ui.setupUi(self)
        self.copyEmployeeUI(self.ui)

    def copyEmployeeUI(self, ui : Ui_EmployeeForm):
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

        self.setup_employee_ui(base_set, 18)

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

    def btnResult_clicked(self):
        isOk, dup_pri_key = self.employees_manager.validation_doubled_abnoma()

        if not isOk:
            msg = QMessageBox()
            msg.setText("アブノーマリティ割当てが重複しています。続行しますか？")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            ans = msg.exec_()

            if ans == QMessageBox.No:
                return

        isOk = self.employees_manager.validation_stared_unassigned_abnoma()

        if not isOk:
            msg = QMessageBox()
            msg.setText("Starされたアブノーマリティに作業が割当たっていません。続行しますか？")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            ans = msg.exec_()

            if ans == QMessageBox.No:
                return


        form = ResultForm()

        result_text = self.employees_manager.get_result_text()

        form.set_text(result_text)
        form.exec_()


