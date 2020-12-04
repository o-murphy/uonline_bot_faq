from telebot import types


def make():
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(types.KeyboardButton(text='Отмена'))
    return kb
