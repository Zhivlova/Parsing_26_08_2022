# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json

import requests
import time
import json

USERNAME = 'Zhivlova'

def get_data(url: str) -> dict:
    while True:
        time.sleep(1)
        response = requests.get(url)
        if response.status_code == 200:
            break
    return response.json()


url = 'https://api.github.com/users/' + USERNAME + '/repos'

response = get_data(url)

repo = []

for item in response:
    repo.append(item['name'])
print(f'Список репозиториев пользователя {USERNAME}')
print(repo)

with open('1_1_repo.json', 'w') as f:
    json_repo = json.dump(repo, f)