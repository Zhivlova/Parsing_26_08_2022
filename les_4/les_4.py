from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
from time import sleep

from pymongo import MongoClient, collection

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36)'

URL_FIRST_PAGE_HH = 'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=developer'

headers = {
    'User-agent': USER_AGENT,
}

def parse_hh(url_page, headers, result=[], index_page=1):
    response = requests.get(url_page, headers=headers)
    if response.status_code !=200:
        print('Парсинг завершен')
        return result
    else:
        print('Страница №%d, ссылка: %s'%(index_page, response.url))


    dom = bs(response.content, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})
    for vacancy in vacancies:
        result.append(parse_vacancy_hh(vacancy))

    link_next_page = dom.find('a', {'data-qa': 'pager-next'})
    if link_next_page:
        link_next_page = 'https://hh.ru' + link_next_page['href']
    else:
        print('Парсинг завершен')
        return result

    result = parse_hh(link_next_page, headers, result, index_page+1)
    return result

def parse_vacancy_hh(dom_vacancy):
    sleep(0.1)
    vacancy_name = dom_vacancy.find('a').text

    vacancy_salary = dom_vacancy.find('span', {'class', 'bloko-header-section-3'})
    if vacancy_salary:
        vacancy_salary = vacancy_salary.text
        min_salary, max_salary, currency_salary = clean_salary(vacancy_salary)
    else:
        min_salary, max_salary, currency_salary = None, None, None

    vacancy_link = dom_vacancy.find('a')['href']

    return {
        'vacancy_name': vacancy_name,
        'vacancy_salary': vacancy_salary,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'currency_salary': currency_salary,
        'vacancy_link': vacancy_link,
        'vacancy_source': 'hh.ru',
    }

def clean_salary(vacancy_salary_text, min_salary=None, max_salary=None, currency_salary=None):
    list_salary = vacancy_salary_text.replace('\u202f', '').split()
    for i in range(len(list_salary) -1):
        if list_salary[i] == 'от':
            min_salary = int(list_salary[i +1])
        elif list_salary[i] == 'до':
            max_salary = int(list_salary[i + 1])
        elif list_salary[i] == '-':
            min_salary = int(list_salary[i - 1])
            max_salary = int(list_salary[i + 1])
    currency_salary = list_salary[-1]

    return min_salary, max_salary, currency_salary

result = parse_hh(URL_FIRST_PAGE_HH, headers)

client = MongoClient()

db = client.vacancies_python_hh

collection_vacancies_hh_ru = db.hh_ru

def cheak_and_save_vacancies_in_db(vacancies):
    for vacancy in vacancies:
        if not len(list(collection_vacancies_hh_ru.find({'vacancy_link': vacancy['vacancy_link']}))):
            collection_vacancies_hh_ru.insert_one(vacancy)


cheak_and_save_vacancies_in_db(result)
result_find = list(collection_vacancies_hh_ru.find())

