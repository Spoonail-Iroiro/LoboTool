import sqlite3
from abnoma_list_scrape import AbnomaListScraper
from portrait_scrape import  AbnomaInfoScraper
from pathlib import Path
from time import sleep
import setting_const as setting
from typing import Callable, Any

root_path = Path(__file__).parent

html_log_dir = root_path / "HTMLLog"
portrait_dir = root_path / "Portrait"

site = "http://ja.lobotomy-corporation.wikia.com"

def get_pri_key(no, feature='latest'):
    former_code = 0

    if feature == 'latest':
        former_code = 0
    else:
        raise Exception("Invalid feature")

    return f"{former_code}-{no}"

def insert_result(cnn, record):
    sql = """
    INSERT INTO m_abnormality 
    (pri_key, no, manage_no, risk_level, name_en, name_ja, name_key, url) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    # VALUES ("0-0", 0, "00-00-00", 2, "rubbit robo", "ウサギロボ","rubbit_robo", "temp");

    cnn.execute(sql, (
        get_pri_key(record["no"]),
        record["no"],
        record["manage_no"],
        record["risk_level"],
        None,
        record["name"],
        None,
        record["url"]))


def init_abnoma_list(web_access=False):
    """
    Lobotomy wikiのトップページのアブノーマリティリストからアブノーマリティ一覧情報を取得しテーブルへinsertする
    ※最新情報を使う場合はlistscrのgetを一度走らせること（ページキャッシュが保存される）
    デフォルトではページキャッシュを用いて情報を抽出する
    :return:
    """
    listscr = AbnomaListScraper("http://ja.lobotomy-corporation.wikia.com/wiki/Lobotomy_Corporation%E6%94%BB%E7%95%A5_Wiki")

    if web_access == True:
        listscr.get()

    all_abnoma_list = listscr.scrape()
    print(all_abnoma_list)

    sample_list = all_abnoma_list

    with sqlite3.connect(str(setting.db_path)) as cnn:
        for record in sample_list:
            insert_result(cnn, record)
        cnn.commit()


def get_abnoma_info(web_access = False, no=None, force=False):
    with sqlite3.connect(str(setting.db_path)) as cnn:

        cnn.row_factory = sqlite3.Row

        select_sql ="""
        SELECT *
        FROM m_abnormality
        
        """

        if web_access and no is None and not force:
            raise Exception("Attempt to Get All abnoma_info. If It's Intended, Set Argument 'force=True'")

        if no is None:
            table = cnn.execute(select_sql)
        else:
            select_sql += " WHERE no = ?"
            table = cnn.execute(select_sql, (no,))

        for row in table:
            url = row["url"]
            absc = AbnomaInfoScraper()
            if web_access:
                #webアクセス許可ならここで（初めて）name_key取得
                name_key = absc.get(site + url)
                sleep(1.5)
            else:
                #不可ならDBから持ってきたものを使う
                name_key = row["name_key"]
                if name_key is None:
                    raise Exception("name_key in DB is Null")
            record = absc.scrape(name_key)
            #終末鳥のギフトはページからとれないので個別対応
            if name_key == "Apocalypse_Bird":
                record["ego_name"] = "Twilight"
            print(record)
            sql = """
            UPDATE m_abnormality
            SET name_en = ?,
            name_key = ?,
            ego_name = ?
            WHERE pri_key = ?
            """
            cnn.execute(sql,(
                record["name_en"],
                record["name_key"],
                record["ego_name"],
                row["pri_key"]
            )
                        )


        cnn.commit()

def bs4_sibling_scrape(start, search_func: Callable[[Any], bool], roop_count = 20):
    sibling = start

    for i in range(roop_count):
        if search_func(sibling) == True:
            return sibling
        sibling = sibling.nextSibling


