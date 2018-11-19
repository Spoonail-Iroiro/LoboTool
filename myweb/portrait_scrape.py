import requests
from bs4 import BeautifulSoup
import db_web_func as db
from pathlib import Path
import setting_const as setting

_global_header = setting.global_header

class AbnomaInfoScraper():
    """
    アブノーマリティ個別ページからアブノーマリティ個別の情報を拾う
    """
    def __init__(self):
        pass

    def get(self, url):
        res = requests.get(url, headers=_global_header)

        if res.status_code != 200:
            ex = Exception(f"http status:{res.status_code}")
            raise ex

        self.html_text = res.text

        #まず各種ファイル名につける名前であるアブノマ名を取得する
        soup = BeautifulSoup(self.html_text, "html.parser")

        name_dict = self.get_local_info(soup)

        name_key = name_dict["name_key"]
        name_en = name_dict["name_en"]

        #取得名を表示
        print("key:", name_key)


        with open( self.get_html_log_path(name_key), "w", encoding="utf-8") as f:
            f.write(self.html_text)

        portrait_url = self.get_portrait_url(soup)

        print("portrait_locatioon:", portrait_url)

        from time import sleep

        sleep(1)

        res = requests.get(portrait_url, headers=_global_header)

        if res.status_code != 200:
            ex = Exception(f"http status:{res.status_code}")
            raise ex

        with open(self.get_portrait_path(name_key), "wb")as fimg:
            fimg.write(res.content)

        self.load(name_key)

        return name_key


    def load(self, name_key):
        with open(self.get_html_log_path(name_key), "r", encoding="utf-8") as f:
            self.html_text = f.read()

        soup = BeautifulSoup(self.html_text, "html.parser")

        self.soup_ = soup

        return soup

    def scrape(self, name_key):

        soup = self.load(name_key)

        name_dict = self.get_local_info(soup)

        print("Done.")

        return name_dict

    def get_local_info(self,soup):
        name_en = self.get_abnoma_name(soup)
        name_key = name_en.replace(" ", "_")
        ego_name = self.get_ego_name(soup)

        return {"name_en":name_en, "name_key":name_key, "ego_name":ego_name}

    def get_abnoma_name(self, soup: BeautifulSoup):
        candi = soup.find_all(class_="page-header__title")

        if len(candi) == 0:
            ex = Exception("Error: Can't Find Name")
            raise ex

        return candi[0].text.strip()

    def get_ego_name(self, soup : BeautifulSoup):
        h3s = soup.find_all("h3")
        target_h3 = None

        for h3 in h3s:
            if h3.span is None:
                continue
            headline = h3.find("span", class_="mw-headline")
            if headline is None:
                continue

            if "観測レベル" in headline.text.strip():
                target_h3 = h3

        if target_h3 == None:
            print("Can't Find 観測レベル Section")
            return None

        sibling = target_h3
        for i in range(10):
            # print(sibling)
            sibling = sibling.nextSibling
            if sibling.name == "dl":
                ego_name = sibling.a.text.strip()
                return ego_name

        print("Can't Find ego name")
        return None


    def get_portrait_url(self, soup):
        h2_all = soup.find_all("h2")
        title_candi = [h2.find("span", class_="mw-headline") for h2 in h2_all]

        story_title_candi = [title for title in title_candi]

        story_title = [title for title in story_title_candi if title and "ストーリー" in title.text]

        if len(story_title) > 1:
            print("WARNING: story_title_candi > 1")

        if len(story_title) == 0:
            #ツール型アブノーマリティは情報欄に肖像ある？
            story_title = [title for title in story_title_candi if title and "情報" in title.text]
            if len(story_title) == 0:
                ex = Exception(f"ERROR: Can't Find story_title\n" + f"{title_candi}")
                raise ex

        idx = story_title_candi.index(story_title[0])

        #ストーリーがタイトルになっているh2要素を拾う
        h2_story = h2_all[idx]

        sibling = h2_story

        while True:
            sibling = sibling.nextSibling
            if sibling.name == "figure":
                img_elem = sibling
                break

        url = img_elem.a.get("href")

        return url
    def get_html_log_path(self, name_key):
        return db.html_log_dir / (name_key + ".html")

    def get_portrait_path(self, name_key):
        return  db.portrait_dir / (name_key + ".png")

