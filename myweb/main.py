import requests
from bs4 import BeautifulSoup
from pathlib import Path
from myweb.portrait_scrape import  AbnomaInfoScraper
from myweb.scrape_cacher import ScrapeCacher
from myweb.abnoma_list_scrape import AbnomaListScraper
import  sqlite3
from time import sleep
import myweb.db_web_func as db
import setting_const as setting
from db_accessor import DBAccessor
import re
from myweb.equipment_egoname_scraper import EquipmentEgonameScraper


global_header = {
    "User-Agent":
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
     }


def data_update():
    # db.get_abnoma_info()
    # db.init_abnoma_list(False)
    # db.get_abnoma_info(True, no=0)
    db.get_abnoma_info(False, no=60)
    # db.get_abnoma_info(True, None, True)

    pass

def test():
    egsc =  EquipmentEgonameScraper()

    records_weapon, _, _ = egsc.scrape()

    print(records_weapon)

    for record_w in records_weapon:
        sql_column_spec = ','.join(record_w.keys())
        sql_value_spec = ','.join(['?' for x in record_w.values()])

        insert_sql = """
        INSERT INTO m_ego_weapon
        ({})
        VALUES
        ({})
        """
        insert_sql = insert_sql.format(sql_column_spec, sql_value_spec)

        with sqlite3.connect(str(setting.db_path)) as cnn:
            cnn.execute(insert_sql, tuple(record_w.values()))








def scrape_all_egoname():
    with sqlite3.connect(str(setting.db_path)) as cnn:
        cnn.row_factory = sqlite3.Row
        select_sql = """
            SELECT *
            FROM m_abnormality
            """
        table = [*cnn.execute(select_sql)]

        for row in table:
            # print(row["name_ja"])
            ego_name = scrape_egoname(row["name_key"])
            if ego_name is None:
                print("abnoma:", row["name_ja"])
            # print(ego_name)



def aptitude_move():
    with sqlite3.connect(str(setting.db_path)) as cnn:
        cnn.row_factory = sqlite3.Row
        select_sql = """
        SELECT *
        FROM m_abnormality
        """
        table = [*cnn.execute(select_sql)]

        for row in table:
            table[""]

def scrape_portrait():
    pass

    # posc = AbnomaInfoScraper()
    #
    # posc.scrape("http://ja.lobotomy-corporation.wikia.com" +  sample_list[1]["url"])


    # res = requests.get("http://ja.lobotomy-corporation.wikia.com" + "/wiki/Training_Standard_Dummy_Rabbit")
    #
    # print(res.text)


def main_get():

    url = "http://ja.lobotomy-corporation.wikia.com/wiki/Training_Standard_Dummy_Rabbit"

    scr_test = ScrapeCacher()

    #scr_test.get(url)

    soup_test = scr_test.load()

    posc = AbnomaInfoScraper()

    name = posc.scrape(url)

# scrape_ego()
# scrape_all_egoname()
# data_update()
test()

