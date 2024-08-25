from telebot import types, TeleBot
import os
from dotenv import load_dotenv

from start_handler import start
from scribd_handler import scribd, scribd_download
from slideshare_handler import slideshare

load_dotenv()
bot = TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def start_bot(message: types.Message):
    start(bot, message.from_user.id)


@bot.message_handler(func=lambda message: message.text == "Scribd 📚")
def start_scribd(message: types.Message):
    scribd(bot, message)


@bot.message_handler(func=lambda message: message.text == "Slideshare 🖥️")
def start_slideshare(message: types.Message):
    slideshare(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call: types.CallbackQuery):
    button_data = call.data
    chat_id = call.from_user.id
    msg_id = call.message.id

    if button_data.startswith("scribd down_"):
        scribd_download(bot, chat_id, msg_id, button_data)


bot.infinity_polling()
