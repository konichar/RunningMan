# -*- coding: utf-8 -*-

import importdir
from flask import Flask, request
# from urllib import unquote_plus
import json
import re
from config import token, debug, heroku_url, bot, telebot
import os


server = Flask(__name__)

importdir.do("features", globals())
import start


@server.route('/', methods=['GET'])
def index():
    return ('This is a website.', 200, None)


@server.route('/monitor/order', methods=['POST'])
def new_order_hook():
    request_object = request.stream.read().decode("utf-8")
    return (request_object, 200, None)


@server.route('/' + token, methods=['POST'])
def getMessage():
    request_object = request.stream.read().decode("utf-8")
    update_to_json = [telebot.types.Update.de_json(request_object)]
    bot.process_new_updates(update_to_json)
    return "got Message bro"


@server.route('/hook')
def webhook():
    jurl = heroku_url
    bot.remove_webhook()
    bot.set_webhook(jurl + token)
    return f"Webhook set to {heroku_url}"


if debug == True:
    bot.remove_webhook()
    bot.polling()
else:
    if __name__ == "__main__":
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))