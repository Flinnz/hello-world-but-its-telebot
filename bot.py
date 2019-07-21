import requests
from time import sleep

url = "https://api.telegram.org/bot763184867:AAE5SQ_RSK082iU1LDM6i5U2-1dk6nOnSjQ/"


def get_updates_json(request):
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', params)
    return response.json()


def last_update(data):
    results = data['result']
    last_update_index = len(results) - 1
    return results[last_update_index]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def send_message(chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            send_message(get_chat_id(last_update(get_updates_json(url))), 'test')
            update_id += 1
        sleep(100)


if __name__ == '__main__':
    main()
