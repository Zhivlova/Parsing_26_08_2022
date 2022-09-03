"""
2. Работа будет состоять с недокументированным API. Нужно ввести релевантный запрос на сайте https://www.delivery-club.ru/search
(а) из предложенных точек с помощью API найти долю (в %) с бесплатной и платной доставкой. Для каждой категории
рассчитать среднюю минимальную стоимость заказа.
(б) для каждой из категорий из пункта (а) рассчитать долю (в %) магазинов и ресторанов
"""
from pprint import pprint

import requests

url = 'https://api.delivery-club.ru/api1.2/vendors/search'

headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36)'
}

params = {
    'latitude': '55.7577374',
    'longitude': '37.6164793',
    'query': 'хачапури'
}

response = requests.get(url=url, headers=headers, params=params)
print(response.status_code)
pprint(f'Найдено {response.json()["found"]} предприятий')


vendors = response.json()['vendors']

all_delivery = []
for vendor in vendors:
    all_delivery.append(vendor['delivery'])

pprint(all_delivery)




