import sqlite3
from typing import  List

class SavAbnomaRecord():
    def __init__(self, pri_key, stared):
        self.pri_key = pri_key
        self.stared = stared

class SavEmployeeRecord():
    def __init__(self, name, work_code, pri_key):
        self.name = name
        self.work_code = work_code
        self.pri_key = pri_key

class DBAccessor:

    cnn: sqlite3.Connection

    def __init__(self, cnn):
        self.cnn = cnn
        self.cnn.row_factory = sqlite3.Row

    def get_abnoma_name_key(self, pri_key):
        row = self.get_abnoma_info_row(pri_key)
        return None if row is None else row["name_key"]

    def get_abnoma_name_ja(self, pri_key):
        row = self.get_abnoma_info_row(pri_key)
        return None if row is None else row["name_ja"]

    def get_abnoma_info_row(self, pri_key):
        select_sql ="""
            SELECT *
            FROM m_abnormality abn
            LEFT OUTER JOIN m_work_aptitude apt
            ON abn.pri_key = apt.abnoma_pri_key
            WHERE pri_key = ?
            """

        result = [*self.cnn.execute(select_sql, (pri_key,))]

        if len(result) > 0:
            return result[0]
        else:
            return None

    def get_abnoma_work_appetitude(self, pri_key):
        row = self.get_abnoma_info_row(pri_key)
        if row is None:
            return None

        rtn = (
            row["inst_code"],
            row["insi_code"],
            row["atta_code"],
            row["supr_code"],
        )

        return rtn

    def update_abnoma_work_appetitude(self, pri_key, inst_code, insi_code, atta_code, supr_code):
        update_work_appetitude_sql = """
            UPDATE m_work_aptitude
            SET inst_code = ?,
            insi_code = ?,
            atta_code = ?,
            supr_code = ?
            WHERE abnoma_pri_key = ?;
            """

        cursor = self.cnn.execute(update_work_appetitude_sql, (inst_code, insi_code, atta_code, supr_code, pri_key))

        if cursor.rowcount > 0:
            return True
        else:
            return False

    def _get_in_phrase(self, list_):
        embraced = [f"'{str(elm)}'" for elm in list_]
        return f"({','.join(embraced)})"

    def get_target_abnoma(self, work_code, app_codes, pri_keys):
        in_target_pri = self._get_in_phrase(pri_keys)
        in_target_app = self._get_in_phrase(app_codes)
        app_column = {
            "00":"inst_code",
            "01":"insi_code",
            "02":"atta_code",
            "03":"supr_code",
        }

        select_sql = """
            SELECT *
            FROM m_abnormality abn
            LEFT OUTER JOIN m_work_aptitude apt
            ON abn.pri_key = apt.abnoma_pri_key
            WHERE {} in {}
            and pri_key in {}        
            """
        select_sql = select_sql.format(app_column[work_code], in_target_app, in_target_pri)

        result = [*self.cnn.execute(select_sql)]

        return result

    #sav_abnomaテーブルを空にして渡された内容を入れる
    def save_sav_abnoma(self, sav_record :  List[SavAbnomaRecord]):
        truncate_sql = """
        DELETE 
        FROM sav_abnormality
        """

        insert_sql = """
        INSERT INTO sav_abnormality
        (idx, pri_key, stared)
        VALUES
        (?, ?, ?)
        """

        self.cnn.execute(truncate_sql)

        for i, record in enumerate(sav_record):
            self.cnn.execute(insert_sql, (i, record.pri_key, 0 if not record.stared else 1))

    def save_sav_employee(self, sav_record: List[SavEmployeeRecord]):
        truncate_sql = """
        DELETE 
        FROM sav_employee
        """

        insert_sql = """
        INSERT INTO sav_employee
        (idx, employee_name, work_code, pri_key)
        VALUES
        (?, ?, ?, ?)
        """

        self.cnn.execute(truncate_sql)

        for i, record in enumerate(sav_record):
            self.cnn.execute(insert_sql, (i, record.name, record.work_code, record.pri_key))

    def get_sav_abnormality(self):
        select_sql = """
        SELECT *
        FROM sav_abnormality
        ORDER BY idx
        """

        table = [*self.cnn.execute(select_sql)]

        return table

    def get_sav_employee(self):
        select_sql = """
        SELECT *
        FROM sav_employee
        ORDER BY idx
        """

        table = [*self.cnn.execute(select_sql)]

        return table

    def get_abnoma_from_pagename(self, pagename : str):
        select_sql = """
        SELECT *
        FROM m_abnormality
        WHERE url LIKE  ("%" || ?)
        """

        table = [*self.cnn.execute(select_sql, (pagename,))]

        if len(table) == 0:
            return None
        else:
            return table[0]

    def insert_ego_weapon(self, id, record):
        insert_sql = """
        INSERT INTO m_ego_weapon
        (pri_key, ego_name, name_ja, name_en)
        VALUES
        (?, ?, ?, ?)
        """

        self.cnn.execute(insert_sql,
                         (id,
                          record["ego_name"],
                          record["name_ja"],
                          record["name_en"]))



