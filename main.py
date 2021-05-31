import pypokedex
import pandas as pd
import numpy as np
from PIL import Image
from pyfiglet import Figlet
from colors import color, cyan # pip install ansicolors
import requests

print("\x1b[2J", end='')

df = pd.read_csv('poke_names.csv')

name_ko = ''

while name_ko != '끝':
    name_ko = input('포켓몬 이름을 입력해주세요: ')
    if len(df.loc[df['name_ko'] == name_ko, 'name_en']) == 0:
        continue
    name_en = df.loc[df['name_ko'] == name_ko, 'name_en'].item()

    print("\x1b[2J", end='')

    p = pypokedex.get(name=name_en)

    img_url = p.sprites.front['default']
    img = np.array(Image.open(requests.get(img_url, stream=True).raw).resize((32, 32)).convert('RGB'), dtype=np.uint8)

    for row in img:
        for pixel in row:
            print(color('  ', bg=f'rgb({pixel[0]}, {pixel[1]}, {pixel[2]})'), end='')
        print()

    print(cyan(Figlet().renderText(f'{p.dex} - {p.name.upper()}')))
    print(Figlet(font='slant').renderText(' / '.join(p.types)))

    def print_stats(iteration, total, prefix='', suffix='', length=100, fill='█'):
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {iteration} {suffix}')

    print_stats(p.base_stats.hp, 100, 'HP ', length=60)
    print_stats(p.base_stats.attack, 100, 'ATK', length=60)
    print_stats(p.base_stats.defense, 100, 'DEF', length=60)
    print_stats(p.base_stats.speed, 100, 'SPD', length=60)