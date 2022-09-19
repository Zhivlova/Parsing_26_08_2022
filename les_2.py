from pprint import pprint
from lxml import html
import requests


def news_parser(url):

    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36)'
    }

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.content)
    articles = dom.xpath('//div')

    articles_dict = {}
    for article in articles:
        title = article.xpath('.//div/h2')[0]
        source = article.xpath('.//div/span[1]/a')[0]
        link = article.xpath('.//div/h2/a')[0]
        date = article.xpath('.//div/span[2]')[0]

    articles_dict[title] = {
        'source': source,
        'link': link,
        'date': date
    }
    return articles_dict

url = 'https://dzen.ru/news/?issue_tld=ru'
yandex = news_parser(url)