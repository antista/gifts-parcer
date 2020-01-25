import sys
import time
from collections import defaultdict

import requests

users = dict()


def get():
    user_id = sys.argv[1]
    response = requests.get(
        'https://api.vk.com/method/gifts.get?user_id=' + user_id + '&v=5.52&access_token=15bf18c6d3e843642027bbdf9e109d820cc71e2b8da4ad15b895ed3f805eccc236956e77ce9a3e13ebe14')
    headers = defaultdict(int, response.json())
    response = headers['response']
    if response == 0:
        print('Подарки пользователя скрыты')
        return
    items = response['items']

    print(f'Всего {response["count"]} подарков', )

    for i in range(min(response['count'], 100)):
        id = str(items[i]['from_id'])
        if id == '0':
            print('Отправитель скрыт')
        else:
            from datetime import datetime
            ts = int(items[i]['date'])
            data = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            message = items[i]['message']
            cont = False
            if id not in users.keys():
                while not cont:
                    try:
                        respons = requests.get(
                            'https://api.vk.com/method/users.get?user_id=' + id + '&v=5.52&access_token=15bf18c6d3e843642027bbdf9e109d820cc71e2b8da4ad15b895ed3f805eccc236956e77ce9a3e13ebe14')
                        header = defaultdict(int, respons.json())
                        if header['response'] == []:
                            cont = True
                            break
                        headers = header['response'][0]
                        users[id] = (headers["first_name"], headers["last_name"])
                        break
                    except:
                        time.sleep(1)
                        continue

            if cont:
                continue
            print(f'Подарок от {users[id][0]} {users[id][1]}')
            print(f'Отправлен: {data}')
            print(f'Сообщение: {message}')
        print('----------------------------------------')
