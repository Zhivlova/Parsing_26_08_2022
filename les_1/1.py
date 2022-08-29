# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json

import requests
from pprint import pprint
import json

url = 'https://github.com/Zhivlova?tab=repositories'

headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36)',
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer'

}

params = {
    'username': 'Zhivlova',
    'tab': 'repositories'
}

response = requests.get(url=url, headers=headers, params=params)
pprint(response.status_code)
names = response.json()['names']
for name in names:
    print(names[''])



