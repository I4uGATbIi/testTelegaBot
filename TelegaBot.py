import telebot
import os
import logging
import psycopg2
from flask import Flask, request

token = "477553068:AAEVHkJonLhCNMcK56v91vFcoD3SKKQUcJI"

bot = telebot.TeleBot(token)
server = Flask(__name__)
logger = logging.getLogger(__file__)

logger.warning("CREATING TABLE!")
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS chats_ids (chat_id int PRIMARY KEY);")
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    logger.warning("START!")
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    try:
        cur.execute("INSERT INTO chats_ids VALUES(" + str(message.chat.id) + ")")
        conn.commit()
    except Exception:
        logger.warning("Already Exists " + str(message.chat.id))


@bot.message_handler(commands=['alertall'])
def alert_all(message):
    logger.warning("Allerting everyone")
    cur.execute("SELECT * FROM chats_ids")
    chats_ids = cur.fetchall()
    for chat_id in chats_ids:
        bot.send_message(chat_id[0], "Произошёл кринж у пользователя - " + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    logger.warning("ANSWER!")
    logger.warning("Adding chat " + str(message.chat.id))
    lol = int(message.chat.id)
    try:
        cur.execute("INSERT INTO chats_ids VALUES(" + str(lol) + ")")
        conn.commit()
    except Exception:
        logger.warning("Already Exists " + str(message.chat.id))
    bot.send_message(message.chat.id, "Здрасьте!Йопт!")


@server.route("/" + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    logger.warning("ANSWER!")
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://calm-temple-62052.herokuapp.com/" + token)
    logger.warning("HOOK!")
    return "!", 200


logger.warning("SERVERSTART!")
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=True)
