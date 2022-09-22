"""
Собрать информацию о вакансиях на вводимую должность с сайтов
hh.ru и/или Superjob и/или работа.ру. Приложение должно
анализировать несколько страниц сайта. Получившийся список
должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (дополнительно: разносим в три поля:
минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например,
работодателя и расположение). Структура должна быть одинаковая
для вакансий с всех сайтов. Общий результат можно вывести с
помощью dataFrame через pandas, сохранить в json, либо csv.
"""
import csv
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests


class SuperJobScrapper:

    def job_search(url):

        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 Safari/537.36)'
        }
        response = requests.get(url=url, headers=headers)
        soup = bs(response.content, 'html.parser')

        data = {
            "title": [],
            "salary": [],
            "link": [],
            "source": []
            }

        try:
            job_title = soup.find_all(class_="_9fIP1 _249GZ _1jb_5 QLdOc")
            for title in job_title:
                titles = title.text.strip()
                data['title'].append(titles)
        except Exception:
            pass

        try:
            all_salaries = soup.find_all(class_="_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi")
            for salary in all_salaries:
                salaries = salary.text.strip()
                data['salary'].append(salaries)
        except Exception:
            pass

        try:
            all_links = soup.find_all(class_="_9fIP1 _249GZ _1jb_5 QLdOc")
            for link in all_links:
                links = 'https://www.superjob.ru/' + link.find('a').get('href')
                data['link'].append(links)
        except Exception:
            pass

        try:
            all_sources = soup.find_all(
                class_="_8zbxf _1bPAn uSWb8")
            for source in all_sources:
                sources = source.text.strip()
                data['source'].append(sources)
        except Exception:
            pass

        result_data = pd.DataFrame(data)

        return result_data


url = 'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4'
python_developer = SuperJobScrapper.job_search(url)

