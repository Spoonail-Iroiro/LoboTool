import requests
from bs4 import BeautifulSoup
from pathlib import Path
from setting_const import risk_level_code

global_header = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

class AbnomaListScraper():
    def __init__(self, url):
        self.url = url
        self.key = "abnoma_list"
        pass

    def scrape(self):
        self.load()

        list = self.get_list(self.soup_)

        return list

    def get(self):
        """
        webへアクセスしてアブノーマリティリストを取得し保存する
        リストの抽出はloadで行うこと（アクセス削減）
        :return:
        """

        res = requests.get(self.url, headers=global_header)

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

    def get_list(self, soup: BeautifulSoup):
        table_candi = soup.find_all("div", class_=["tabber", "tabberlive"])
        table_candi = [table.find("div", class_="tabbertab").div for table in table_candi ]
        table_candi = [table for table in table_candi if (table and ("アブノーマリティ" in table.b.text))]

        if len(table_candi) == 0:
            ex = Exception("Can't Find abnoma_list")
            raise ex

        table = table_candi[0].parent.find("table")
        table = table.find_all("tr")

        # print(table)
        print(len(table))

        list_ = [row.find_all("td") for row in table if len(row.find_all("td")) == 7]
        #日本語名
        name_list_ = [row_td[3].text.strip() for row_td in list_]
        #ページurl
        url_list = [row_td[2].a.get("href") for row_td in list_]
        #No（※厳密な通し番号ではなく管理番号の3番目、ただしハゲは59）
        no_list = [row_td[0].text.strip() for row_td in list_]
        #管理番号
        manage_no_list = [row_td[4].text.strip() for row_td in list_]
        risk_level_list = [row_td[6].a.get("title").strip() for row_td in list_]
        risk_level_list = [risk_level_code[level_str] for level_str in risk_level_list]

        key_list = ["no", "manage_no", "risk_level", "name", "url"]

        zipped = zip(no_list, manage_no_list, risk_level_list, name_list_, url_list)

        result_dicts = [dict(zip(key_list, zip_)) for zip_ in zipped]

        return result_dicts

    def get_html_log_path(self):
        return db_web.html_log_dir / (self.key + ".html")


