import requests
import re
from bs4 import BeautifulSoup

class PokemonSpider:
    def __init__(self, id, url, server):
        self.id = id
        self.url = url
        self.server = server
    def fetchData(self):
        print(self.id, self.url)
        req = requests.get(url=self.url)
        html = req.text
        html = BeautifulSoup(html, "html.parser")
        tables = html.find_all('table', class_=re.compile("roundy a-r at-c"))
        table = tables[0]
        trs = table.find_all('tr')

        # index = 0
        # for each in trs:
        #     print("=============================: {}".format(index))
        #     print(each)
        #     index=index+1

        image_tr = trs[2]
        type_category_tr = trs[4]
        # self.__parse_type_category(type_category_tr)
        ability_tr = trs[9]
        # self.__parse_ability(ability_tr)
        exp_100_tr = trs[12]
        # self.__parse_exp_100(exp_100_tr)
        height_weight_tr = trs[30]
        self.__parse_height_weight(height_weight_tr)

    def __parse_type_category(self, tr):
        tds = tr.find_all('td')
        type_td = tds[0]
        type_category = tds[3]
        type_as = type_td.find_all('a')
        type_as = type_as[1:]
        for each in type_as:
            type=each.string
            type=type.lstrip()
            type=type.rstrip()
            type=self.__typeOfTypeCN(type)
            url = self.server + each.get('href')
            print('===>type: '+type, url)
            #TODO 记录 type 要爬的链接到某个文件

        category_tds = type_category.find_all('td', class_=re.compile("bw-1"))
        category_td = category_tds[0]
        category = category_td.string
        print('===>category: '+category) #TODO 把 category 翻译成英文

    def __parse_ability(self, tr):
        table = tr.find_all('table', class_='roundy bgwhite fulltable')[0]
        tds = table.find_all('td')

        ability_td = tds[0]
        hidden_ability_td = tds[1]

        ability_as = ability_td.find_all('a')
        for each in ability_as:
            ability = each.string
            ability=ability.lstrip()
            ability=ability.rstrip()
            ability=self.__typeOfAbilityCN(ability)
            url = self.server+each.get('href')
            print("ability: "+ability, url)

        hidden_ability_as = hidden_ability_td.find_all('a')
        for each in hidden_ability_as:
            hidden_ability = each.string
            hidden_ability=hidden_ability.lstrip()
            hidden_ability=hidden_ability.rstrip()
            url = self.server+each.get('href')
            print("hidden_ability: "+hidden_ability, url)

    def __parse_exp_100(self, tr):
        table = tr.find_all('table', class_='roundy bgwhite fulltable')[0]
        exp_100_td = table.find_all('td')[0]
        exp_100 = exp_100_td.string
        exp_100=exp_100.lstrip()
        exp_100=exp_100.rstrip()
        print("exp_100: "+exp_100)
        return

    def __parse_height_weight(self, tr):
        tables = tr.find_all('table', class_='roundy bgwhite fulltable')
        height_table = tables[0]
        weight_table = tables[1]
        height_td = height_table.find_all('td')[0]
        weight_td = weight_table.find_all('td')[0]
        height = height_td.string
        height=height.lstrip()
        height=height.rstrip()
        weight = weight_td.string
        weight=weight.lstrip()
        weight=weight.rstrip()
        print("height: "+height)
        print("weight: "+weight)

    def __typeOfTypeCN(self, type):
        if (type == '一般'):
            return 'normal'
        elif (type == '虫'):
            return 'bug'
        elif (type == '毒'):
            return 'poison'
        elif (type == '飞行'):
            return 'flying'
        elif (type == '地面'):
            return 'ground'
        elif (type == '格斗'):
            return 'fighting'
        elif (type == '妖精'):
            return 'fairy'
        elif (type == '恶'):
            return 'dark'
        elif (type == '龙'):
            return 'dragon'
        elif (type == '冰'):
            return 'ice'
        elif (type == '超能力'):
            return 'psychic'
        elif (type == '电'):
            return 'electric'
        elif (type == '草'):
            return 'grass'
        elif (type == '水'):
            return 'water'
        elif (type == '火'):
            return 'fire'
        elif (type == '钢'):
            return 'steel'
        elif (type == '幽灵'):
            return 'ghost'
        elif (type == '岩石'):
            return 'rock'
        else :
            return type

    def __typeOfAbilityCN(self, ability):
        #TODO: 爬https://wiki.52poke.com/wiki/特性列表，生成一个字典来存中文->英文
        if (ability == '恶臭'):
            return 'stench'
        else :
            return ability
