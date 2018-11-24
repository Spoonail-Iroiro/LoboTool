import sys

risk_level_code = {
    "ZAYIN":1,
    "TETH":2,
    "HE":3,
    "WAW":4,
    "ALEPH":5,
}

inv_risk_level_code = {v:k for k, v in risk_level_code.items()}

work_code = {
    "本能":"00",
    "洞察":"01",
    "愛着":"02",
    "抑圧":"03",
}

inv_work_code = {v:k for k,v in work_code.items()}

work_code_to_btnWork = {
    "00":"btnInstinct",
    "01":"btnInsight",
    "02":"btnAttachment",
    "03":"btnSuppression",
}

inv_work_code_to_btnWork = { v:k for k, v in work_code_to_btnWork.items() }

appetitude_code = {
    "不適":"00",
    "適性あり":"01",
    "100以上で適性あり":"02",
}

damage_type_code = {
    "RED":0,
    "WHITE":1,
    "BLACK":2,
    "PALE":3,
    "???":4,
}

inv_appetitude_code = {v:k for k, v in appetitude_code.items()}

from pathlib import Path

resource_dir = Path(sys.argv[0]).parent / "Resource"

db_path = resource_dir / "team.sdb"

portrait_dir = resource_dir / "Portrait"

import sqlite3
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt


class GlobalAsset:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                cls._instance._singleton_init()
            except Exception:
                cls._instance = None
                raise
        return cls._instance

    def _singleton_init(self):
        self.is_loaded = False

        self.thumbnails1 = {}
        self.stared_img = None
        self.selected_img = None

    def load(self):
        if self.is_loaded:
            return
        if QApplication.instance() is None:
            raise Exception("QApplication Instance Doesn't Exist. Can't Load QPixmap.")

        with sqlite3.connect(str(db_path)) as cnn:
            # cnn.row_factory = sqlite3.Row
            select_sql = """
            SELECT name_key
            FROM m_abnormality
            """
            name_key_table = cnn.execute(select_sql)
            for row in name_key_table:
                name_key = row[0]
                pixmap = QPixmap()
                pixmap.load(str(portrait_dir / (name_key + ".png")))
                pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)

                self.thumbnails1[name_key] = pixmap

        selected_pix = QPixmap()
        selected_pix.load(str(resource_dir / "circle.png"))
        self.selected_img = selected_pix

        stared_pix = QPixmap()
        stared_pix.load(str(resource_dir / "stared.png"))
        self.stared_img = stared_pix

        self.is_loaded = True

global_header = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

print(resource_dir)
