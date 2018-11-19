import requests
from bs4 import BeautifulSoup
from pathlib import Path

global_header = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

class ScrapeCacher():
    def __init__(self):
        pass

    def get(self, url, local="tmp.html"):
        res = requests.get(url, headers=global_header)

        if res.status_code != 200:
            ex = Exception(f"HTTP Status:{res.status_code}")
            raise ex

        with open(local, "w", encoding="utf-8") as f:
            f.write(res.text)

    def load(self, local="tmp.html"):
        with open(local, "r", encoding="utf-8") as f:
            self.text_ = f.read()
            self.soup = BeautifulSoup(self.text_, "html.parser")

        return self.soup

    def save_image(self, url, filename):
        res = requests.get(url, headers=global_header)

        if res.status_code != 200:
            ex = Exception(f"HTTP Status:{res.status_code}")
            raise ex

        with open(filename, "wb", encoding="utf-8") as f:
            f.write(res.content)
