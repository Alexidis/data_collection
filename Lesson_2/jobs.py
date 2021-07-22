import requests
from pathlib import Path
from bs4 import BeautifulSoup as Bs
import pandas as pd
from fake_headers import Headers

header = Headers(headers=True).generate()
vacancy_data = {'vacancy_name': '',     # Наименование вакансии
                'salary': '',           # Предлагаемую зарплату (отдельно минимальную и максимальную)
                'link': '',             # Ссылка на саму вакансию
                'site': '',             # Сайт, откуда собрана вакансия
                "employer_name": '',    # Наименование работодателя
                'employer_city': ''     # Расположение работодателя
                }


# Функции примерно одинаковые, по этому комметы оставлю только в одной
def get_hh(prof, page_count):
    SITE_NAME = 'https://hh.ru'
    search_results_text = ''

    # Получаем результаты поиска с заданного кол-ва страниц
    for page in range(page_count):
        url = f'{SITE_NAME}/search/vacancy?area=53&fromSearchLine=true&st=searchVacancy&text={prof}&page={page}'
        search_results = requests.get(url, headers=header)
        search_results.encoding = 'UTF-8'
        search_results_text += search_results.text

    # Если результаты есть
    if search_results_text:
        formatted_vacancies = []
        vacancy_classes = {'items': "vacancy-serp-item",
                           'name': 'resume-search-item__name',
                           'salary': {'class': 'bloko-header-section-3 bloko-header-section-3_lite',
                                      'data-qa': 'vacancy-serp__vacancy-compensation'},
                           "employer_name": 'vacancy-serp-item__meta-info-company',
                           'employer_city': {'class': 'vacancy-serp-item__meta-info',
                                             'data-qa': 'vacancy-serp__vacancy-address'}}

        # Создаем парсер
        soup = Bs(search_results_text, 'lxml')
        # Выбираем конкретные записи поиска
        vacancies = soup.find_all(class_=vacancy_classes['items'])

        for vacancy in vacancies:
            # Создаем новый и на полняем новый словарь
            vd = vacancy_data.copy()
            vd['vacancy_name'] = vacancy.find(class_=vacancy_classes['name']).text

            # ЗП может быть не всегда указана по этому делаем промежуточное значение
            meta_sal = vacancy.find(attrs=vacancy_classes['salary'])
            vd['salary'] = meta_sal.text if meta_sal else 'ЗП не указана'
            vd['link'] = vacancy.find(class_=vacancy_classes['name']).a.get('href')
            vd['site'] = SITE_NAME
            vd["employer_name"] = vacancy.find(class_=vacancy_classes['employer_name']).text
            vd['employer_city'] = vacancy.find(attrs=vacancy_classes['employer_city']).text

            formatted_vacancies.append(vd)

    return formatted_vacancies


def get_superjob(prof, page_count):
    SITE_NAME = 'https://superjob.ru'
    search_results_text = ''

    for page in range(1, page_count + 1):
        url = f'{SITE_NAME}/vacancy/search/?keywords={prof}&page={page}'
        search_results = requests.get(url, headers=header)
        search_results_text += search_results.text

    if search_results_text:
        formatted_vacancies = []
        vacancy_classes = {'items': 'f-test-search-result-item',
                           'name': '_1h3Zg _2rfUm _2hCDz _21a7u',
                           'salary': '_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW',
                           "employer_name": '_1h3Zg _3Fsn4 f-test-text-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc',
                           'employer_city': '_1h3Zg f-test-text-company-item-location e5P5i _2hCDz _2ZsgW'}

        soup = Bs(search_results_text, 'lxml')
        # Дополнительно убираем рекламу
        vacancies = [elem for elem in soup.find_all(class_=vacancy_classes['items'])
                     if elem.find(class_=vacancy_classes['name']) is not None]

        for vacancy in vacancies:
            vd = vacancy_data.copy()
            vd['vacancy_name'] = vacancy.find(class_=vacancy_classes['name']).text

            vd['salary'] = vacancy.find(class_=vacancy_classes['salary']).text
            vd['link'] = SITE_NAME + vacancy.find(class_=vacancy_classes['name']).a.get('href')
            vd['site'] = SITE_NAME
            vd["employer_name"] = vacancy.find(class_=vacancy_classes['employer_name']).text
            vd['employer_city'] = vacancy.find(class_=vacancy_classes['employer_city']).text.split(' • ')[-1]

            formatted_vacancies.append(vd)

    return formatted_vacancies


if __name__ == '__main__':
    prof = input("Введите название профессии: ")
    page_count = int(input("Введите количество страниц для поиска: "))

    # Поиск на двух сайтах
    hh_res = pd.DataFrame(get_hh(prof, page_count))
    superjob_res = pd.DataFrame(get_superjob(prof, page_count))

    # Объединение результатов
    pd_res = pd.concat([superjob_res, hh_res], ignore_index=True)
    # Сохранение в файл
    vacancies_path = Path.cwd() / 'output/jobs.csv'
    pd_res.to_csv(vacancies_path, encoding='UTF-8')

    # Вывод в консоль
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(pd_res)
