from telebot import types, TeleBot


def start(bot: TeleBot, chat_id: int):
    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Scribd 📚")
    btn2 = types.KeyboardButton("Slideshare 🖥️")
    main_markup.row(btn1, btn2)
    bot.send_message(
        chat_id,
        "You can use this bot to download scribd and slideshare books for free. All you need is the document link.",
        reply_markup=main_markup,
    )
