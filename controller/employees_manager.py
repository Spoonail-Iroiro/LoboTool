from controller.employee_controller import EmployeeController
import sqlite3
import setting_const as setting
from db_accessor import DBAccessor, SavAbnomaRecord, SavEmployeeRecord

class EmployeesManger():
    def __init__(self):
        #管理対象のemployee_controllers
        self._controllers = []
        pass

    def add_controller(self, controller):
        controller.set_parent_manager(self)
        self._controllers.append(controller)

    #参照するAbnomasManagerを指定
    def connect_AbnomasManager(self, abnomas_manager):
        self.abnomas_manager = abnomas_manager

    #収容アブノーマリティのpri_keyを取得
    def get_abnoma_pri_keys(self):
        return self.abnomas_manager.get_abnoma_pri_keys()

    #登録されているcontrollerのuiをセットアップする
    def setupui(self):
        #コンポーネント個別のsetupはcontrollerにやらせる
        for con in self._controllers:
            con.setupui()
            # 作業登録更新時のイベント登録
            con.work_registered.connect(self.work_register_updated)
            con.work_unregistered.connect(self.work_register_updated)

    def work_register_updated(self):
        pri_keys = [con.abnoma_pri_key for con in self._controllers if con.abnoma_pri_key is not None]
        self.abnomas_manager.update_abnoma_select(pri_keys)

    def validation_doubled_abnoma(self):
        check_list = []

        for con in self._controllers:
            if con.abnoma_pri_key is None:
                continue
            if con.abnoma_pri_key in check_list:
                return False, con.abnoma_pri_key
            else:
                check_list.append(con.abnoma_pri_key)

        return True, None

    def validation_stared_unassigned_abnoma(self):
        stared_abnoma_pri_keys = self.abnomas_manager.get_stared_abnoma_pri_keys()
        assigned_abnoma_pri_keys = [con.abnoma_pri_key for con in self._controllers if con.abnoma_pri_key is not None]

        ft_list = [stared in assigned_abnoma_pri_keys for stared in stared_abnoma_pri_keys]

        return all(ft_list)

    def get_result_text(self):
        result_text = ""
        with sqlite3.connect(str(setting.db_path)) as cnn:
            #アブノーマリティ基準で列挙する
            for assigned_pri_key in self.abnomas_manager.get_assigned_abnoma_pri_keys():
                #対称のアブノーマリティに割り当たっているエージェントのControllerだけ抽出
                assigned_employee = [en_con for en_con in self._controllers if en_con.abnoma_pri_key == assigned_pri_key]

                for assigned_con in assigned_employee:
                    acc = DBAccessor(cnn)

                    name = acc.get_abnoma_name_ja(assigned_con.abnoma_pri_key)
                    work_name = setting.inv_work_code[assigned_con.work_code]

                    result_text += f"{name}→{assigned_con.employee_name}（{work_name}）\n\n"
        return result_text


    #現在の収容アブノーマリティ・作業登録状態をセーブする
    def save(self):
        records_abnoma = self.abnomas_manager.get_sav_abnoma_records()
        records_employee = [SavEmployeeRecord(con.ui_set["ledEmployee"].text(), con.work_code, con.abnoma_pri_key) for con in self._controllers]
        with sqlite3.connect(str(setting.db_path)) as cnn:
            acc = DBAccessor(cnn)
            acc.save_sav_abnoma(records_abnoma)
            acc.save_sav_employee(records_employee)

    def load(self):
        with sqlite3.connect(str(setting.db_path)) as cnn:
            acc = DBAccessor(cnn)
            table_abnoma = acc.get_sav_abnormality()
            table_employee = acc.get_sav_employee()

            self.abnomas_manager.load(table_abnoma)

            for record, con in zip(table_employee, self._controllers):
                if record["work_code"] is None:
                    continue
                con: EmployeeController
                con.register_work(record["work_code"], record["pri_key"])
                con.ui_set["ledEmployee"].setText(record["employee_name"])

