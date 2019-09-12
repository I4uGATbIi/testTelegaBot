import telebot
import os
import logging
from flask import Flask, request
# from telegram.ext import Updater

token = "477553068:AAEVHkJonLhCNMcK56v91vFcoD3SKKQUcJI"

bot = telebot.TeleBot(token)
server = Flask(__name__)
logger = logging.getLogger(__file__)


@bot.message_handler(commands=['start'])
def start(message):
    logger.warning("START!")
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    logger.warning("ANSWER!")
    bot.reply_to(message, message.text)


@server.route("/" + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    logger.warning("ANSWER!")
    return "!", 200


@server.route("/")
def webhook():
    # PORT = int(os.environ.get('PORT', '8443'))
    # updater = Updater(token)
    # updater.start_webhook(listen='0.0.0.0',
    #                       port=PORT,
    #                       url_path=token)
    bot.remove_webhook()

    bot.set_webhook(url="https://calm-temple-62052.herokuapp.com/" + token)
    # updater.idle()
    logger.warning("HOOK!")
    return "!", 200


logger.warning("SERVERSTART!")
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
webhook()
