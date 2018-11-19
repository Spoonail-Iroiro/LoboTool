from setting_const import *
from PySide2.QtWidgets import QPushButton, QWidget, QTableView
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QTextEdit, QTextEdit, QTextEdit
from PySide2.QtCore import QRect, QPoint
from typing import Callable, Any

def get_relative_pos(widget_src : QWidget, widget_dst : QWidget):
    return widget_dst.geometry().topLeft() - widget_src.geometry().topLeft()

def move_by_relative_pos(widget : QWidget, relative : QPoint):
    orig_pos = widget.geometry().topLeft()

    widget.move(orig_pos + relative)

def set_size_by_widget(widget: QWidget, ref_size_widget: QWidget):
    widget.setFixedSize(ref_size_widget.geometry().size())

def get_selected_table_row(tv : QTableView, datasource):
    sel_model = tv.selectionModel()
    selections = sel_model.selectedRows()

    if len(selections) == 0:
        return None
    else:
        row_index = selections[0].row()
        rtn = datasource[row_index]
        return rtn


