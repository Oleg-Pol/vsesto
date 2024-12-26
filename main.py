import requests, time, random, datetime
import pandas as pd
from bs4 import BeautifulSoup
url = 'https://www.vsesto.by/'
items_urls = []
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
}
table_columns = ['Название', 'Адрес', 'Контакты', 'Рабочие дни', 'Рабочее время', 'Сайт']
table = {column: [] for column in table_columns}
# https://kwork.ru/projects/2470874/view
def get_data():
    with open('urls.txt', 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()
    for url in urls[:20]:
        # url = 'https://www.vsesto.by/sto/45820/'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
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
            en_num = sit[st_num+6:].find('"')
            sit = sit[st_num+6: st_num+6 + en_num]
        except Exception as ex:
            sit = 'Нет сайта'

        # table_columns = ['Название', 'Адрес', 'Контакты', 'Рабочие дни', 'Рабочее время', 'Сайт']
        table['Название'].append(tittle)
        table['Адрес'].append(adress)
        table['Контакты'].append(telephone)
        table['Рабочие дни'].append(work_days)
        table['Рабочее время'].append(work_time)
        table['Сайт'].append(sit)
        print(work_days)
        print(work_time)
        print(tittle)
        print(adress)
        print(telephone)
        print((sit))
        print('-'*20)

    # fonts = soup.find_all('font')
    # for font in fonts:
    #     try:
    #         print(font.get('size'))
    #         # if int(font.get('size')) == 2:
    #         #     print(font.text)
    #     except:
    #         pass

def fuck():
    a= ['5']
    url = 'https://www.vsesto.by/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.find_all('div')
    for div in divs:
        if div.get('style') is not None:
            if 'padding-top: 5px; padding-left: ' in div.get('style'):
                print(div.text.strip())
                if div.text.strip() in a:
                    print(f'ПИЗДЕЦ!!! {div.text.strip()}')
                a.append(div.text.strip())
    for page in range(2, 17):
        url = f'https://www.vsesto.by/p/{page}/'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        divs = soup.find_all('div')
        for div in divs:
            if div.get('style') is not None:
                if 'padding-top: 5px; padding-left: ' in div.get('style'):
                    print(div.text.strip())
                    if div.text.strip() in a:
                        print(f'ПИЗДЕЦ!!! {div.text.strip()}')
                    a.append(div.text.strip())
def pizdec():
    count = 1
    url = 'https://www.vsesto.by/sitemap/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('a', class_='name_novis_l')
    for item in items[292:1013]:
        print(count, item.text)
        href = 'https://www.vsesto.by' + item.get('href')
        with open('721_urls.txt', 'a', encoding='utf-8') as file:
            file.write(href + '\n')
        count +=1
def main():
    # get_data()
    # cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    # pd.DataFrame(table).to_excel(f'{cur_time}.xlsx')
    pizdec()
def get_urls():

    url_list = ['https://www.vsesto.by/sto-zavodskogo-raiona/', 'https://www.vsesto.by/sto-leninskogo-raiona/', 'https://www.vsesto.by/sto-moskovskogo-raiona/', 'https://www.vsesto.by/sto-oktyabrskogo-raiona/', 'https://www.vsesto.by/sto-partizanskogo-raiona/', 'https://www.vsesto.by/sto-pervomayskogo-raiona/', 'https://www.vsesto.by/sto-sovetskogo-raiona/', 'https://www.vsesto.by/sto-frunzenskogo-raiona/', 'https://www.vsesto.by/sto-tsentralnogo-raiona/', 'https://www.vsesto.by/sto-uruche/', 'https://www.vsesto.by/sto-malinovka/', 'https://www.vsesto.by/sto-masukovshhina/', 'https://www.vsesto.by/sto-shabany/', 'https://www.vsesto.by/sto-zelenyj-lug/']
    for url in url_list[:5]:
        count = 1
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for element in soup.find_all('a', class_='name_novis'):
            if element.get('target') == '_blank':
                href = 'https://www.vsesto.by' + element.get('href')
                print(count, element.text, href)
                count +=1


if __name__ == '__main__':
    main()
















# response = requests.get(url, headers=headers)
    # # print(response.text)
    # soup = BeautifulSoup(response.text, 'lxml')
    # all_items = soup.find_all('a', class_='name_novis')
    # for i in range(132, 164):
    #     href = 'https://www.vsesto.by' + all_items[i].get('href')
    #     with open('urls.txt', 'a', encoding='utf-8') as file:
    #         file.write(href + '\n')
    #     items_urls.append(href)
    # for page in range(16, 17):
    #     url = f'https://www.vsesto.by/p/{page}/'
    #     response = requests.get(url, headers=headers)
    #     time.sleep(random.randint(1, 3))
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     imtes = soup.find_all('a', class_='name_novis')
    #     for i in range(132, 153):
    #         href = 'https://www.vsesto.by' + imtes[i].get('href')
    #         print(imtes[i].text, href)
    #         with open('urls.txt', 'a', encoding='utf-8') as file:
    #             file.write(href + '\n')
    #     # for i in range(len(imtes)):
    #     #     print(i, imtes[i].text)