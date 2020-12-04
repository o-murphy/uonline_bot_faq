from telebot import types


def make():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(text='В меню', callback_data='to_start'),
           types.InlineKeyboardButton(text='Не помогло', callback_data='sup'))
    return kb