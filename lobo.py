import sys

from setting_const import *
from forms.team_form import TeamForm
import shutil

if __name__ == "__main__":

    app = QApplication(sys.argv)

    #アセットのロード
    assets = GlobalAsset()
    assets.load()

    form = TeamForm()

    form.load()

    form.show()

    app.exec_()

    #セーブのバックアップ
    shutil.copy(db_path, db_path.parent / "bak_team.sdb")

    form.save()
