import setting_const as sc
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit, QLineEdit
from PySide2.QtCore import QRect, Signal, QObject

from my_qt_util import *
import functools
from db_accessor import DBAccessor

class EmployeeController(QObject):
    work_registered = Signal()
    work_unregistered = Signal()

    def __init__(self, id, ui_set, base_set):
        super().__init__()
        self.id = id
        #ターゲットアブノーマリティのpri_key
        self.abnoma_pri_key = None
        #登録している作業
        self.work_code = None
        self.ui_set = ui_set
        self.base_set = base_set
        # self._get_pri_keys_func = get_pri_keys_func

    def set_parent_manager(self, manager):
        self.manager = manager

    def setupui(self):
        x_gap = 400
        y_gap = 140
        #1列に入る欄の数
        column_content = 6

        base_pos_widget = self.base_set["ledEmployee"]
        for k in self.ui_set:
            #すべてのウィジェット共通で縦に並べる
            any_wid : QWidget = self.ui_set[k]
            any_base_wid :QWidget = self.base_set[k]
            #一度base_objまで移動
            any_wid.setGeometry(any_base_wid.geometry())
            #複数個あるので縦横に並べる
            gap = QPoint(int(self.id / column_content) * x_gap, y_gap * (self.id % column_content))
            move_by_relative_pos(any_wid, gap)

            if k.startswith("txt"):
                img : QLineEdit = self.ui_set[k]
                base_obj : QLabel = self.base_set[k]
                img.setFont(base_obj.font())

            if k.startswith("btn"):
                btn: QPushButton = self.ui_set[k]
                base_obj : QPushButton = self.base_set[k]
                set_size_by_widget(btn, base_obj)
                btn.setText(base_obj.text())

            #イベントハンドラの設定
            if k in ["btnInstinct", "btnInsight", "btnSuppression", "btnAttachment"]:
                btn: QPushButton = self.ui_set[k]
                btn.clicked.connect(functools.partial(self.btnWork_clicked,inv_work_code_to_btnWork[k]))

            if k == "btnClear":
                btn: QPushButton = self.ui_set[k]
                btn.clicked.connect(self.unregister_work)


    def btnWork_clicked(self, work_code):
        from forms.select_target_form import SelectTargetForm
        #managerのメソッドでアブノーマリティの一覧を取得/
        pri_keys = self.manager.get_abnoma_pri_keys()
        form = SelectTargetForm(work_code, pri_keys)
        form.exec_()

        if form.result_pri_key is not None:
            self.register_work(work_code, form.result_pri_key)
        pass


    def register_work(self, work_code, pri_key):
        self.work_code = work_code
        self.abnoma_pri_key = pri_key

        with sqlite3.connect(str(sc.db_path)) as cnn:
            acc = DBAccessor(cnn)
            name = acc.get_abnoma_name_ja(pri_key)
            work_name = sc.inv_work_code[work_code]
            abnoma_text = f"{name}（{work_name}）"
            self.ui_set["txtAbnoma"].setText(abnoma_text)

        self.work_registered.emit()

    def unregister_work(self):
        self.work_code = None
        self.abnoma_pri_key = None
        self.ui_set["txtAbnoma"].setText("")
        # self.ui_set["ledEmployee"].setText("")

        self.work_unregistered.emit()

    @property
    def employee_name(self):
        return self.ui_set["ledEmployee"].text()
