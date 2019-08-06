import os
import re
import requests
import json
from bottle import run, post, get, request, BaseResponse


class Bot:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.update_id = -1

    def set_webhook(self, webhook_url):
        params = {'url': webhook_url}
        resp = requests.post(self.api_url + "setWebhook", data=params)
        return resp

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        resp = requests.post(self.api_url + 'sendMessage', data=params)
        return resp


my_bot_token = os.environ.get('BOT_KEY')
bot = Bot(my_bot_token)
bot.set_webhook("https://hello-world-but-its-a-telebot.herokuapp.com/bot")
help_regex = re.compile(r'[п][о][м][о][щ][ь]', re.

updates = []

@post('/viberCallback')
def callback():
    updates.append(request.json)
    return BaseResponse(status=200)

@post('/bot')
def hook():
    update = request.json
    current_chat_id = update['message']['chat']['id']
    sent_message = update['message']['text']
    if re.match(help_regex, sent_message):
        sent_message = 'Сам себе помоги'
    elif sent_message[-1] == '?':
        sent_message = sent_message[0:len(sent_message) - 1] + '.'
    elif sent_message.lower() == 'анекдот':
        sent_message = 'тут был плохой анек'
    update_id = update['update_id']
    if update_id >= bot.update_id or bot.update_id == -1:
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
