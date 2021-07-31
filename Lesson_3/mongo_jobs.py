from Lesson_2 import get_hh
from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
db = client['jobs']
vacancy = db['vacancy']


def insert_vac(vac_list):
    pattern = '\d+[\d|\s]*'

    for vac in vac_list:

        # Заполняем вилку ЗП если возможно
        salary_fork = re.findall(pattern, vac['salary'])
        salary = {'min': 0, 'max': 0}
        if len(salary_fork):
            salary['min'] = int(re.sub('\s', '', salary_fork[0]))
            salary['max'] = int(re.sub('\s', '', salary_fork[-1]))

        # Добавляем новые записи если их нет иначе обновляем
        vacancy.update_many(
            {'link': vac['link']},
            {'$set':
                {
                    'vacancy_name': vac['vacancy_name'],
                    'salary': {'origin_salary': vac['salary'],
                               'min_salary': salary['min'],
                               'max_salary': salary['max']
                               },
                    'site': vac['site'],
                    'employer_name': vac["employer_name"],
                    'employer_city': vac['employer_city']
                }
            },
            upsert=True
        )


def get_well_paid(good_money):
    result_vac = vacancy.find({'salary.min_salary': {'$gte': good_money}})
    for doc in result_vac:
        print(doc)


if __name__ == '__main__':
    prof = input("Введите название профессии: ")
    page_count = int(input("Введите количество страниц для поиска: "))

    vacancies = get_hh(prof, page_count)
    insert_vac(vacancies)

    desired_salary = int(input("Введите желаемую зарплату: "))
    get_well_paid(desired_salary)
