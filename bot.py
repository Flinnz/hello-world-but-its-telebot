import os

import requests
from bottle import route, run, post, request, response, BaseResponse

my_bot_token = os.environ.get('BOT_KEY')


class Bot:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.update_id = -1

    def get_updates_json(self, req):
        params = {'timeout': 100, 'offset': None}
        resp = requests.get(req + 'getUpdates', params)
        return resp.json()

    def last_update(self, data):
        results = data['result']
        last_update_index = len(results) - 1
        return results[last_update_index]

    def set_webhook(self, webhook_url):
        params = {'url': webhook_url}
        resp = requests.post(self.api_url + "setWebhook", data=params)
        return resp

    def get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        resp = requests.post(self.api_url + 'sendMessage', data=params)
        return resp


bot = Bot(my_bot_token)
bot.set_webhook("https://hello-world-but-its-a-telebot.herokuapp.com/bot")


@post('/bot')
def hook():
    update = request.json
    current_chat_id = bot.get_chat_id(update)
    sent_message = update['message']['text']
    update_id = update['update_id']
    if update_id == bot.update_id or bot.update_id == -1:
        bot.send_message(current_chat_id, sent_message)
        bot.update_id += 1
    return BaseResponse(status=200)


if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    host = '0.0.0.0'
else:
    port = 5000
    host = '127.0.0.1'

if __name__ == '__main__':
    run(host=host, port=port)
