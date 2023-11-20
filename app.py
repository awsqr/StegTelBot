import telebot
import credential
import StegEngine
import cv2
from telebot.types import InputFile
import os

bTOKEN = credential.TOKEN

bot = telebot.TeleBot(bTOKEN)

image_path = 0

blank_image = 0

secret_message = 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello. I can be used to encode secret messages to images.\nTo start select a command.")

@bot.message_handler(commands=['encode'])
def send_encode(message):
    sent_msg = bot.reply_to(message, "Now send the message you would like to encode.")
    bot.register_next_step_handler(sent_msg, store_message)

def store_message(message):
    global secret_message
    secret_message = message.text
    sent_msg = bot.reply_to(message, "Now select an image")
    bot.register_next_step_handler(sent_msg, send_encoded_image)

@bot.message_handler(commands=['decode'])
def send_decode(message):
    sent_msg = bot.reply_to(message, "Got it. Please send encoded photo.")
    bot.register_next_step_handler(sent_msg, send_decoded_message)

def send_decoded_message(message):
    raw = message.photo[2].file_id
    path = raw+".png"
    image_path = bot.get_file(raw)
    secret_image = bot.download_file(image_path.file_path)
    with open(path,'wb') as new_file:
        new_file.write(secret_image)
    decoded_message = StegEngine.decode(path)
    bot.reply_to(message, decoded_message[:20])
    os.remove(path)


def send_encoded_image(message):
    output_image = "image_1.PNG"
    raw = message.photo[2].file_id
    path = raw+".png"
    global image_path
    image_path = bot.get_file(raw)
    global blank_image
    blank_image = bot.download_file(image_path.file_path)
    with open(path,'wb') as new_file:
        new_file.write(blank_image)
    encoded_image = StegEngine.encode(path, secret_message)
    if(cv2.imwrite(output_image, encoded_image)):
        bot.send_photo(message.chat.id, InputFile(output_image))
    else:
        bot.reply_to(message, "failed to encode image.")
    os.remove(output_image)
    os.remove(path)

@bot.message_handler(func=lambda msg: True)
def default(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.infinity_polling()

