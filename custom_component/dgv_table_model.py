from typing import List, Any
from PySide2.QtCore import QAbstractTableModel
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
import setting_const as setting
from typing import Callable

class AbstractDGVColumn(object):
    def __init__(self, data_key, header_text = None):
        self.data_key = data_key
        self.header_text = data_key if header_text is None else header_text

    def get_content(self, role, datasource_value):
        raise NotImplementedError()

class DGVColumn(AbstractDGVColumn):
    def __init__(self, data_key, header_text = None, format_func = None):
        super().__init__(data_key, header_text)
        self.format_func = format_func

    def get_content(self, role, datasource_value):
        if role == Qt.DisplayRole:
            return datasource_value if self.format_func is None else self.format_func(datasource_value)


class DGVImageColumn(AbstractDGVColumn):
    def __init__(self, data_key, header_text = None, get_image_func: Callable[[Any], QPixmap] = None):
        super().__init__(data_key, header_text)
        if get_image_func is None:
            raise Exception("Set get_image_func")
        self.get_image_func = get_image_func
        self._pics = setting.GlobalAsset().thumbnails1

    def get_content(self, role, datasource_value):
        if role == Qt.DecorationRole:
            pixmap = self.get_image_func(datasource_value)
            return pixmap

class AbnomaThumbnailColumn(DGVImageColumn):
    def __init__(self, data_key, header_text=None):
        super().__init__(data_key, header_text, self.get_abnoma_thumbnail)
        self._pics = setting.GlobalAsset().thumbnails1

    def get_abnoma_thumbnail(self, name_key):
        return self._pics[name_key]



class DGVTableModel(QAbstractTableModel):
    dgv_columns: List[AbstractDGVColumn]

    def __init__(self):
        super().__init__()
        self.dgv_columns = []
        self._datasource = []

    def rowCount(self, parent):
        if parent.isValid():
            return 0

        return len(self._datasource)

    def columnCount(self, parent):
        if parent.isValid():
            return 0

        return len(self.dgv_columns)

    def data(self, index, role):
        if not index.isValid():
            return None

        col_key = self.dgv_columns[index.column()].data_key
        try:
            datasource_value = self._datasource[index.row()][col_key]
        except:
            print(col_key)
        content = self.dgv_columns[index.column()].get_content(role, datasource_value)
        return content

        # if role == Qt.DisplayRole:
        #     col_key = self.dgv_columns[index.column()].data_key
        #     return self._datasource[index.row()][col_key]
        # elif role == Qt.DecorationRole and index.column() == 0:
        #     asset = setting.GlobalAsset()
        #     name_key = self._datasource[index.row()]["name_key"]
        #     pixmap = asset.thumbnails1[name_key]
        #     return pixmap

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                header_text = self.dgv_columns[section].header_text
                return header_text


    def clear_datasource(self):
        self.layoutAboutToBeChanged.emit()
        self.modelAboutToBeReset.emit()
        self._datasource = []
        self.modelReset.emit()
        self.layoutChanged.emit()

    def bind_datasource(self, datasource : List[Any]):
        self.layoutAboutToBeChanged.emit()
        self.modelAboutToBeReset.emit()
        self._datasource = datasource
        self.modelReset.emit()
        self.layoutChanged.emit()

    def add_column(self, dgv_column : AbstractDGVColumn):
        self.layoutAboutToBeChanged.emit()
        self.modelAboutToBeReset.emit()

        self.dgv_columns.append(dgv_column)

        self.modelReset.emit()
        self.layoutChanged.emit()

    def clear_column(self):
        self.layoutAboutToBeChanged.emit()
        self.modelAboutToBeReset.emit()
        self.dgv_columns = []
        self.modelReset.emit()
        self.layoutChanged.emit()

    def get_datasource(self):
        return self._datasource




