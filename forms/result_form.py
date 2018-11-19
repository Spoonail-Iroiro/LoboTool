from forms.result_form_ui import Ui_ResultForm
from PySide2.QtWidgets import QDialog

class ResultForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ResultForm()
        self.ui.setupUi(self)

    def set_text(self, txt):
        self.ui.txtMain.setPlainText(txt)

