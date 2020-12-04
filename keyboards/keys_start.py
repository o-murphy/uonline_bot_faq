from telebot import types


def make():
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(types.InlineKeyboardButton(text="FAQ", callback_data="faq"),
           types.InlineKeyboardButton(text="Справка", callback_data="help"),
           types.InlineKeyboardButton(text="Контакты", callback_data="contact"))
    return kb
