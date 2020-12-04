from telebot import types


def make():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(types.InlineKeyboardButton(text='В меню', callback_data='to_start'),
           types.InlineKeyboardButton(text='Нет, спросить у поддержки',
                                      callback_data='sup'))
    return kb
