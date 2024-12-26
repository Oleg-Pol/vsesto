import time, random, datetime
import pandas as pd
from bs4 import BeautifulSoup
import asyncio
import aiohttp

items_urls = []
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
}
table_columns = ['Название', 'Адрес', 'Контакты', 'Рабочие дни', 'Рабочее время', 'Сайт']
table = {column: [] for column in table_columns}
count = 1
async def get_tasks():
    with open('neu.txt', 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()
    async with asyncio.TaskGroup() as group:
        for url in urls:
            group.create_task(get_data(url))
async def get_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                global count
                time.sleep(0.2)
                soup = BeautifulSoup(await response.text(), 'lxml')
                tittle = soup.find('h1', class_='title2').text
                # print(tittle)
                divs = soup.find_all('div')
                tru_divs = []
                for div in divs:
                    if div.get('style') == 'padding-top: 4px;':
                        tru_divs.append(div)

                adress = (tru_divs[1].find_all('font')[1].text.strip())
                tels = soup.find_all('a', class_='tel')
                telephone = ', '.join([tel.text for tel in tels])
                for div in divs:
                    if div.get('style') == 'padding-top: 6px; padding-bottom: 5px;':
                        nobr = div
                nobr = nobr.find('nobr').find_all('img')

                work_days = ''
                if nobr[0].get('src') == '/images/rab.png':
                    work_days += 'Пн'
                if nobr[1].get('src') == '/images/rab.png':
                    work_days += ', Вт'
                if nobr[2].get('src') == '/images/rab.png':
                    work_days += ', Ср'
                if nobr[3].get('src') == '/images/rab.png':
                    work_days += ', Чт'
                if nobr[4].get('src') == '/images/rab.png':
                    work_days += ', Пт'
                if nobr[5].get('src') == '/images/rab.png':
                    work_days += ', Сб'
                if nobr[6].get('src') == '/images/rab.png':
                    work_days += ', Вс'

                divs = soup.find_all('div')
                for div in divs:
                    if div.get('style') == 'padding-top: 6px; padding-bottom: 5px;':
                        work_times = div
                work_times = work_times.find_all('font')
                for i in range(len(work_times)):
                    if work_times[i].text == 'Рабочие дни: ':
                        time_in = i + 1
                        break
                work_time = work_times[time_in].text
                try:
                    for div in divs:
                        if div.get('style') == 'padding-top: 6px; padding-bottom: 5px;':
                            sit = div.find('script').text
                    st_num = sit.find('href')
                    en_num = sit[st_num + 6:].find('"')
                    sit = sit[st_num + 6: st_num + 6 + en_num]
                except Exception as ex:
                    sit = 'Нет сайта'

                # table_columns = ['Название', 'Адрес', 'Контакты', 'Рабочие дни', 'Рабочее время', 'Сайт']
                table['Название'].append(tittle)
                table['Адрес'].append(adress)
                table['Контакты'].append(telephone)
                table['Рабочие дни'].append(work_days)
                table['Рабочее время'].append(work_time)
                table['Сайт'].append(sit)
                if (count % 10) == 0:
                    print(f'[+] {count}')
                count += 1
    except:
        print(url)

def main():
    asyncio.run(get_tasks())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    pd.DataFrame(table).to_excel(f'{cur_time}.xlsx')
if __name__ == '__main__':
    main()