import telebot
import os
import logging
from DatabaseConn import Database
from flask import Flask, request

token = "477553068:AAEVHkJonLhCNMcK56v91vFcoD3SKKQUcJI"

bot = telebot.TeleBot(token)
server = Flask(__name__)
logger = logging.getLogger(__file__)
db = Database()


@bot.message_handler(commands=['start'])
def start(message):
    logger.warning("START!")
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    try:
        conn = db.getConnection()
        users = conn["users"]
        query = {"chatId": message.chat.id}
        foundUser = users.find(query)
        if foundUser.retrieved < 1:
            user = {"userId": message.from_user.id, "firstName": f'{message.from_user.first_name}',
                    "lastName": f'{message.from_user.last_name}', "userName": f'{message.from_user.username}',
                    "chatId": message.chat.id}
            logger.warning(user)
            users.insert(user)
        else:
            logger.warning("Chat already remembered!")
    except Exception as e:
        logger.warning("Something went wrong\n" + e.__str__())


@bot.message_handler(commands=['alertall'])
def alert_all(message):
    logger.warning("Allerting everyone")
    try:
        users = db.getConnection()['users']
        for user in users.find():
            logger.warning("Sending to " + str(user["chatId"]))
            try:
                bot.send_message(user["chatId"], "Произошёл кринж у пользователя - " + message.from_user.first_name)
                bot.send_photo(user["chatId"],
                               'https://cs8.pikabu.ru/images/big_size_comm/2016-01_4/1453051436159957875.jpg')
            except Exception:
                logger.warning("Chat " + str(user["chatId"]) + " OHUEL")
    except Exception as e:
        dblist = db.getClient().list_database_names()
        if "telegram" not in dblist:
            print("The database not exists.")
        else:
            logger.warning(e.__str__())


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    logger.warning("ANSWER!")
    logger.warning("Adding chat " + str(message.chat.id))
    try:
        conn = db.getConnection()
        users = conn["users"]
        query = {"chatId": message.chat.id}
        foundUser = users.find(query)
        if foundUser.retrieved < 1:
            user = {"userId": message.from_user.id, "firstName": f'{message.from_user.first_name}',
                    "lastName": f'{message.from_user.last_name}', "userName": f'{message.from_user.username}',
                    "chatId": message.chat.id}
            logger.warning(user)
            users.insert(user)
        else:
            logger.warning("Chat already remembered!")
    except Exception as e:
        logger.warning("Something went wrong\n" + e.__str__())
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
