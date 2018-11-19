import requests
from bs4 import BeautifulSoup
import bs4
from pathlib import Path
from setting_const import risk_level_code
import myweb.db_web_func as db
import setting_const as setting
import re

_global_header = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

class EquipmentEgonameScraper():
    def __init__(self):
        self.key = "ego"
        pass

    def scrape(self):
        self.load()

        records = self._get_ego(self.soup_)

        return records

    def get(self):
        """
        webへアクセスしてEGOページを取得し保存する
        抽出はloadで行うこと（アクセス削減）
        :return:
        """
        url = "http://ja.lobotomy-corporation.wikia.com/wiki/Equipment"

        res = requests.get(url, headers=_global_header)

        if res.status_code != 200:
            ex = Exception(f"http status:{res.status_code}")
            raise ex

        with open(self.get_html_log_path(), "w", encoding="utf-8") as f:
            f.write(res.text)

        self.load()


    def load(self):

        with open(self.get_html_log_path(), "r", encoding="utf-8") as f:
            self.html_text = f.read()

        soup = BeautifulSoup(self.html_text, "html.parser")

        self.soup_ = soup

    def _get_ego(self, soup: BeautifulSoup):
        h3s = soup.find_all("h3")

        #結果をrecordに入れて返す
        records_weapon = []
        records_suit = []
        records_gift = []

        for i, h3 in enumerate(h3s):
            record_weapon = { "pri_key":i }
            record_suit = { "pri_key":i }
            record_gift = { "pri_key":i }

            if h3.find("span", class_="mw-headline") is None:
                continue

            h3 : bs4.element.Tag

            #見出しからEGO名を抽出
            titlestring = h3.span.text
            print(titlestring)
            result = re.search(r"（([\x21-\x7e\s]+)、(.*)）", titlestring)
            #名前は共通
            for record in [record_weapon, record_suit, record_gift]:
                record["ego_name"] = result.group(1).strip()
                record["name_en"] = record["ego_name"]
                record["name_ja"] = result.group(2).strip()
            print(record_weapon["ego_name"], record_weapon["name_ja"])

            #見出し下の武器・スーツ・ギフト見出しからそれぞれ抽出

            def sibling_search_func(sibling):
                if sibling.name == "div" and "mw-collapsible" in sibling["class"]:
                    return True

            content = db.bs4_sibling_scrape(h3, sibling_search_func)

            #下線が引いてあるところ　あとは後ろでキーワードマッチ
            ego_type_titles = [child for child in content.children if child.name is not None and len(child.find_all("u")) != 0]

            for title in ego_type_titles:
                if "武器：" in title.text :
                    def table_search(sibling):
                        if sibling.name == "table":
                            return True

                    info_table = db.bs4_sibling_scrape(title, table_search)

                    rows = info_table.find_all("tr")
                    info_row_cells = rows[1].find_all("td")
                    #リスクレベルは0列目
                    risk_level_text = info_row_cells[0].text.strip()
                    record_weapon["risk_level"] = risk_level_code[risk_level_text]
                    record_weapon["cost"] = info_row_cells[1].text.strip()
                    record_weapon["capacity"] = info_row_cells[2].text.strip()

                    # record_weapon["damage"] =
                    record_weapon.update(self._parse_weapon_damage(info_row_cells[3].text.strip()))
                    record_weapon["attack_freq"] = info_row_cells[4].text.strip()
                    #揃ったら追加
                    records_weapon.append(record_weapon)

        return records_weapon, records_suit, records_gift




    def _parse_weapon_damage(self, text):
        print(text)
        parsed = re.search(r"([A-Za-z?]+).*\(([\d]+)[-\s]*([\d]+)\)", text)
        result = {}
        result["damage_type"] = setting.damage_type_code[parsed.group(1)]
        result["min_damage"] = int(parsed.group(2))
        result["max_damage"] = int(parsed.group(3))

        return result

















    # with sqlite3.connect(str(setting.db_path)) as cnn:
    #
    #
    #         acc = DBAccessor(cnn)
    #         acc.insert_ego_weapon(i, record)
    def get_html_log_path(self):
        return db.html_log_dir / (self.key + ".html")


