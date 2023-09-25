import telebot
import credential

bTOKEN = credential.TOKEN

bot = telebot.TeleBot(bTOKEN)

@bot.message_handler(commands=['start'])
def send_encode(message):
    bot.reply_to(message, "Hello. I can be used to encode secret messages to images.\nTo start select a command.")


@bot.message_handler(commands=['encode'])
def send_encode(message):
    bot.reply_to(message, f"You have selected {message.text}")

@bot.message_handler(commands=['decode'])
def send_decode(message):
    bot.reply_to(message, f"You have selected {message.text}")

@bot.message_handler(func=lambda msg: True)
def default(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()