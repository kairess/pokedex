# Reference: https://github.com/heejongahn/pokedex/blob/master/pokedex/crawl.py
import requests
from lxml import html
import pandas as pd

url = 'https://pokemon.fandom.com/ko/wiki/국가별_포켓몬_이름_목록'

r = requests.get(url)
doc = html.fromstring(r.content)

table = doc.cssselect('div.WikiaArticle table.prettytable')[0]
rows = table.cssselect('tr')[1:]

df = pd.DataFrame(columns=['dex', 'name_ko', 'name_en'])

for i, row in enumerate(rows):
    tds = row.findall('td')

    dex = None

    try:
        dex = int(tds[0].text.strip())
    except Exception as e:
        print(e)
    
    name_ko = tds[1].getchildren()[0].text.strip()
    name_en = tds[3].text.strip().lower()

    print(i, dex, name_ko, name_en)

    df = df.append({'dex': dex, 'name_ko': name_ko, 'name_en': name_en}, ignore_index=True)

print(df)

df.to_csv('poke_names.csv', index=False)
