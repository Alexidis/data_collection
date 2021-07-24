import requests
from pathlib import Path
from lxml import html
import pandas as pd
from fake_headers import Headers

header = Headers(headers=True).generate()
news_tmpl = {'source_name': '',     # Наименование источника
             'title': '',           # Наименование новости
             'link': '',            # Ссылку на новость
             'p_date': ''           # Дата публикации
             }

# Параметры всех источников
sources = {
    'mail.ru':
        {'url': 'https://news.mail.ru',
         'main_path': '//*[@class="list__text"]',
         'attrs': {
             'title': './text()',
             'link': './@href'}
         },
    'lenta.ru':
        {'url': 'https://lenta.ru/',
         'main_path': '//*[@class="item"]/a',
         'attrs': {
             'title': './text()',
             'link': './@href',
             'p_date': './time/@datetime'}
         },
    'yandex.ru':
        {'url': 'https://yandex.ru/news/',
         'main_path': '//*[starts-with(@class, "mg-grid__col mg-grid__col_xs_")]',
         'attrs': {
             'title': './article/div[1]/div[1]/div/text()',
             'link': './article/div[1]/div[1]/a/@href',
             'p_date': './article/div[2]/div[1]/div/span[2]/text()'}
         }
}

# Список новостей из всех источников
newspaper = []
for source_key, source_val in sources.items():
    # Параметры одной новости
    news = news_tmpl.copy()
    # Список новостей одного источника
    source_news = []

    response = requests.get(source_val['url'], headers=header)
    parsed = html.fromstring(response.text)

    # Задаем имя источника
    news['source_name'] = source_key

    # Выбираем основные новости
    for item in parsed.xpath(source_val['main_path']):
        # Парсим необходимые параметры
        for attr_name, attr_val in source_val['attrs'].items():
            attr = item.xpath(attr_val)
            news[attr_name] = attr[0] if attr else ''

        # Если новость спарсилась неправильно, добавлять ее не будем
        if news['title'] != '':
            source_news.append(news.copy())

    # Агрегируем новости
    newspaper.extend(source_news)

newspaper_df = pd.DataFrame(newspaper)
# Сохранение в файл
vacancies_path = Path.cwd() / 'output/nespaper.csv'
newspaper_df.to_csv(vacancies_path, encoding='UTF-8')

# Вывод в консоль
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(newspaper_df)
