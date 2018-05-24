import requests
import re
from bs4 import BeautifulSoup

class PokemonSpider:
    def __init__(self, id, url):
        self.id = id
        self.url = url
    def fetchData(self):
        print(self.id, self.url)
        req = requests.get(url=self.url)
        html = req.text
        html = BeautifulSoup(html, "html.parser")
        tables = html.find_all('table', class_=re.compile("roundy a-r at-c"))
        table = tables[0]
        trs = table.find_all('tr')

        # for each in trs:
        #     print("=============================")
        #     print(each)

        image_tr = trs[2]
        type_category_tr = trs[4]
        self.__parse_type_category(type_category_tr)

    def __parse_type_category(self, tr):
        tds = tr.find_all('td')
        type_td = tds[0]
        type_category = tds[3]
        type_as = type_td.find_all('a')
        type_as = type_as[1:]
        for each in type_as:
            type=each.string
            print('===>type: '+type)

        category_tds = type_category.find_all('td', class_=re.compile("bw-1"))
        category_td = category_tds[0]
        category = category_td.string
        print('===>category: '+category)
