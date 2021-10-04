import telebot
from models import *
TOKEN = "1258084373:AAFnxvjZ67Gx4iMROrCtyk21h981G-4xJWE"
bot = telebot.TeleBot(TOKEN, parse_mode=None)




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "Are you horny right now?")
    with open("horny.mp4", "rb") as f:
        bot.send_video(message.chat.id,f)


if __name__ == "__main__":
    bot.infinity_polling()
    session.close()