from setting_const import *
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit
from PySide2.QtCore import QRect
from my_qt_util import *
import functools
import  sqlite3
from db_accessor import DBAccessor

from forms.select_abnoma_form import SelectAbnomaForm

class AbnomaController():

    def __init__(self, id, ui_set, base_set):
        self.ui_set = ui_set
        self.base_set = base_set
        self.id = id
        self.pri_key = None
        self.selected = False
        self.stared = False

    def btnRegister_clicked(self):
        form = SelectAbnomaForm()

        form.exec_()

        if form.result_pri_key is not None:
            self.register_abnoma(form.result_pri_key)

        if form.result_is_reset == True:
            self.unregister_abnoma()


    def setupui(self):
        #uiは各部門へ位置は移動された状態
        k : str
        base_pos_widget = self.base_set["imgAbnoma"]
        for k in self.ui_set:
            if k.startswith("img"):
                img : QLabel = self.ui_set[k]
                base_obj : QLabel = self.base_set[k]
                #位置は調整済みのため、サイズのみbaseに合わせる
                rect = QRect(img.geometry())
                rect.setSize(base_obj.geometry().size())
                img.setGeometry(rect)

                asset = GlobalAsset()
                if k.startswith("imgAbnoma"):
                    img.setText("未登録")

                if k.startswith("imgSelected"):
                    selected_pix = asset.selected_img.scaled(img.size(), Qt.KeepAspectRatio)
                    img.setPixmap(selected_pix)
                    img.hide()

                if k.startswith("imgStared"):
                    stared_pix = asset.stared_img.scaled(img.size(), Qt.KeepAspectRatio)
                    img.setPixmap(stared_pix)
                    img.hide()


                # rect.moveTop(img.geometry().top())
                # tmp[k].setGeometry(rect)

            if k.startswith("btn"):
                btn: QPushButton = self.ui_set[k]
                base_obj : QPushButton = self.base_set[k]
                relative_pos = get_relative_pos(base_pos_widget, base_obj)
                move_by_relative_pos(btn, relative_pos)
                set_size_by_widget(btn, base_obj)
                # btn.geometry())
                btn.setText(base_obj.text())
                btn.setFont(base_obj.font())

        self.ui_set["btnRegister"].clicked.connect(self.btnRegister_clicked)
        self.ui_set["btnStar"].clicked.connect(self.btnStar_clicked)


    def btnStar_clicked(self):
        img = self.ui_set["imgStared"]
        if self.stared:
            self.stared = False
            img.hide()

        else:
            self.stared = True
            img.show()

    def select_abnoma(self):
        self.selected = True
        img = self.ui_set["imgSelected"]
        img.show()

    def unselect_abnoma(self):
        self.selected = False
        img = self.ui_set["imgSelected"]
        img.hide()

    def register_abnoma(self, pri_key):
        #pri_key更新
        self.pri_key = pri_key

        #アイコン表示を更新
        img_abnoma : QLabel = self.ui_set["imgAbnoma"]
        with sqlite3.connect(str(db_path)) as cnn:
            acc = DBAccessor(cnn)
            name_key = acc.get_abnoma_name_key(pri_key)

            pix = GlobalAsset().thumbnails1[name_key].scaled(img_abnoma.size(), Qt.KeepAspectRatioByExpanding)
            img_abnoma.setPixmap(pix)

    def unregister_abnoma(self):
        self.pri_key = None
        img_abnoma : QLabel = self.ui_set["imgAbnoma"]
        img_abnoma.setText("未登録")



