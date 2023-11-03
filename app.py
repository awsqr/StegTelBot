import telebot
import credential
import StegEngine
import cv2

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
    bot.reply_to(message, "Now select an image")

@bot.message_handler(commands=['decode'])
def send_decode(message):
    image_path = bot.get_file(message.photo.file_id)
    secret_image = bot.download_file(image_path.file_path)
    decoded_message = StegEngine.decode(secret_image)
    bot.reply_to(message, decoded_message)

@bot.message_handler(content_types=['photo'])
def send_encoded_image(message):
    raw = message.photo[2].file_id
    path = raw+".png"
    global image_path
    image_path = bot.get_file(raw)
    global blank_image
    blank_image = bot.download_file(image_path.file_path)
    with open(path,'wb') as new_file:
        new_file.write(blank_image)
    encoded_image = StegEngine.encode(image_path.file_path, secret_message)

    bot.reply_to(message, encoded_image)

@bot.message_handler(func=lambda msg: True)
def default(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()