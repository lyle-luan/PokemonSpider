import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
import os, os.path

if __name__ == '__main__':

    if os.path.exists("./PokemonData/Generation.json"):
        os.remove("./PokemonData/Generation.json")
    if os.path.exists("./i18n/Localization/zh.js"):
        os.remove("./i18n/Localization/zh.js")
    if os.path.exists("./i18n/Localization/en.js"):
        os.remove("./i18n/Localization/en.js")
    if os.path.exists("./i18n/Localization/ja.js"):
        os.remove("./i18n/Localization/ja.js")

    genJson = open("./PokemonData/Generation.json", "a")
    zhJS = open("./i18n/Localization/zh.js", "a")
    enJS = open("./i18n/Localization/en.js", "a")
    jaJS = open("./i18n/Localization/ja.js", "a")

    genJson.write("{")
    zhJS.write("export default {")
    enJS.write("export default {")
    jaJS.write("export default {")

    server = 'https://wiki.52poke.com/'

    target = 'https://wiki.52poke.com/wiki/宝可梦列表（按全国图鉴编号）/简单版'
    req = requests.get(url=target)
    html = req.text
    bf_table = BeautifulSoup(html, "html.parser")
    br_td = bf_table.find_all('table', class_ = 'a-c roundy eplist bgl-一般 b-一般 bw-2')[0]
    br_td = br_td.find_all('td')

    is_sn = 0 #0表示读到 sn，1表示读到中文，2是日文，3是英文
    poke_sn = ''
    poke_name_cn = ''
    poke_name_ja = ''
    poke_name_en = ''
    poke_url = ''

    isFirstGen = True

    for each in br_td:
        if 'colspan' in each.attrs:
            a = each.find_all('a')[0]
            gen = a.string
            gen_pinyin = ''
            gen_pinyin_list = lazy_pinyin(gen)
            for each in gen_pinyin_list:
                gen_pinyin = gen_pinyin + each
            if isFirstGen:
                isFirstGen = False
                genJson.write("\""+gen_pinyin+"\":[") #"diyishidai":[
            else:
                genJson.write("],") #"diyishidai":[
                genJson.write("\""+gen_pinyin+"\":[") #"diyishidai":[
        else :
            if is_sn == 0:
                is_sn += 1
                poke_sn = each.string
                poke_sn = poke_sn.lstrip()
                poke_sn = poke_sn[1:4]
            elif is_sn == 1:
                is_sn += 1
                a = each.find_all('a')[0]
                poke_name_cn = a.string
                poke_url = server + a.get('href')
            elif is_sn == 2:
                is_sn += 1
                a = each.find_all('a')[0]
                poke_name_ja = a.string
            elif is_sn == 3:
                is_sn = 0
                a = each.find_all('a')[0]
                poke_name_en = a.string
                poke_name_pinyin = ''
                poke_name_pinyin_list = lazy_pinyin(poke_name_cn)
                for each in poke_name_pinyin_list:
                    poke_name_pinyin = poke_name_pinyin + each
                poke_id = 'a'+poke_sn+'_'+poke_name_pinyin
                genJson.write("{\"key\":\""+poke_id+"\"},") #{"key":"id"},
                zhJS.write(poke_id+":'"+poke_name_cn+"',")
                enJS.write(poke_id+":'"+poke_name_en+"',")
                jaJS.write(poke_id+":'"+poke_name_ja+"',")


                print(poke_id, poke_name_ja, poke_name_en, poke_url)

    genJson.write("}")
    genJson.close()
    zhJS.write("};")
    zhJS.close()
    enJS.write("};")
    enJS.close()
    jaJS.write("};")
    jaJS.close()
