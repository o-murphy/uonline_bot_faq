from telebot import types


def cancel():
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(types.KeyboardButton(text='Отмена'))
    return kb


def support():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.row(types.InlineKeyboardButton(text='В меню', callback_data='to_start'),
           types.InlineKeyboardButton(text='Нет, спросить у поддержки',
                                      callback_data='sup'))
    return kb


def phone():
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    kb.add(types.KeyboardButton(text='Отправить телефон', request_contact=True),
           types.KeyboardButton(text='Отмена'))
    return kb


def remove():
    kb = types.ReplyKeyboardRemove()
    return kb


def reply():
    kb = types.ForceReply()
    return kb


def to_start():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(text='В меню', callback_data='to_start'))
    return kb


def start():
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(types.InlineKeyboardButton(text="FAQ", callback_data="faq"),
           types.InlineKeyboardButton(text="Справка", callback_data="help"),
           types.InlineKeyboardButton(text="Контакты", callback_data="contact"))
    return kb


def make_close():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(types.InlineKeyboardButton(text='Закрыть',
                                      callback_data='close'))
    return kb


def make_open():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.row(types.InlineKeyboardButton(text='Открыть снова', callback_data='open'))
    return kb
