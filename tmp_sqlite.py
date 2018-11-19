from PySide2.QtWidgets import QApplication, QLabel
import sqlite3
from pathlib import Path
from setting_const import GlobalAsset
import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit
from PySide2.QtCore import QRect
from my_qt_util import *

def qpixmap_prac():

    app = QApplication(sys.argv)

    asset = GlobalAsset()
    asset.load()
    pics = asset.thumbnails1

    print(asset.thumbnails1["Big_Bird"])

    label = QLabel()
    label.setPixmap(pics["Big_Bird"])

    label.show()

    app.exec_()

app = QApplication(sys.argv)

rect1 = QRect(100, 50,200,50)
rect2 = QRect(200,150,50,50)
rect3 = QRect(300,300,1,1)

#rect1を基準としたrect2への相対位置を取得
relative_pos = rect2.topLeft() - rect1.topLeft()
print(relative_pos)

rect3_copy = QRect(rect3)

#moveは絶対位置指定
rect3_copy.moveTopLeft(relative_pos)
print(rect3_copy.topLeft())

#相対位置分移動させたければもともとのposに足す
rect3.moveTopLeft(rect3.topLeft() + relative_pos)
print(rect3)

rect3.setSize(rect2.size())
print(rect3)

label_target = QLabel()
rect_label_target = QRect(300, 300, 1, 1)
label_target.setGeometry(rect_label_target)
label1 = QLabel()
label1.setGeometry(rect1)
label2 = QLabel()
label2.setGeometry(rect2)

relative_pos = get_relative_pos(label1, label2)
move_by_relative_pos(label_target, relative_pos)
set_size_by_widget(label_target, label1)
print(label_target.geometry())






