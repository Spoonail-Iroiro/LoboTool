try:
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

except Exception as ex:
    import sys, traceback
    with open("err.txt","w",encoding="utf-8") as f:
        exec, ms, tb = sys.exc_info()
        traceback.print_exc(file=f)
        raise ex

