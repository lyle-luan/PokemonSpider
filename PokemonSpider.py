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
        # self.__parse_height_weight(height_weight_tr)
        catch_rate_tr = trs[40]
        # self.__parse_catch_rate(catch_rate_tr)
        gender_ratio_tr = trs[45]
        # self.__parse_gender_ratio(gender_ratio_tr)
        egg_groups_hatch_time_tr = trs[50]
        self.__parse_egg_groups_hatch_time(egg_groups_hatch_time_tr)

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

    def __parse_catch_rate(self, tr):
        table = tr.find_all('table', class_='roundy bgwhite fulltable')[0]
        td = table.find_all('td')[0]
        catch_rate = td.contents[0]
        catch_rate=catch_rate.lstrip()
        catch_rate=catch_rate.rstrip()
        print("catch_rate: "+catch_rate)

    def __parse_gender_ratio(self, tr):
        table = tr.find_all('table', class_='roundy bw-1 bgwhite fulltable')[0]
        td = table.find('td')
        tds = td.find_all('td')

        no_gender_td = tds[0]
        unknown_gender_td = tds[1]
        gender_td = tds[3]

        if 'hide' in no_gender_td:
            print("is_no_gender: true")
        elif 'hide' in unknown_gender_td:
            print("is_unknown_gender: true")
        else:
            spans = gender_td.find_all('span')
            male_span = spans[0]
            female_span = spans[1]
            male = male_span.string
            female = female_span.string
            male = male[3:]
            female = female[3:]
            print("gender_ratio_male: "+male)
            print("gender_ratio_female: "+female)

    def __parse_egg_groups_hatch_time(self, tr):
        table = tr.find('table', class_='roundy bgwhite fulltable')
        tds = table.find_all('td')
        egg_groups_td = tds[0]
        hatch_time_td = tds[1]
        egg_groups_as = egg_groups_td.find_all('a')

        egg_groups = []
        for each in egg_groups_as:
            egg_group = each.string
            egg_groups.append(egg_group)

        last_egg_group = egg_groups[-1]
        last_egg_group = last_egg_group[:-1]
        egg_groups[-1] = last_egg_group

        for each in egg_groups:
            print("egg_group: "+each)

        hatch_time = hatch_time_td.get_text()
        hatch_time=hatch_time.lstrip()
        hatch_time=hatch_time.rstrip()
        hatch_time_detail = hatch_time.split(' ')
        hatch_time_cycle = hatch_time_detail[0]
        print("hatch_time_cycle: "+hatch_time_cycle)
        hatch_time_step_detail = hatch_time_detail[1]
        hatch_time_step = hatch_time_step_detail[5:-2]
        print("hatch_time_step: "+hatch_time_step)

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
