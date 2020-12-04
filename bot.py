import json
import os
import re
import time

import telebot

from keyboards import keys_start, keys_sup, key_phone, key_remove, key_reply, key_cancel
from modules import ask, phone, support, info

abspath = os.path.abspath(__file__)
d_name = os.path.dirname(abspath)
os.chdir(d_name)

with open('modules/config.json', 'r') as cfg:
    config = json.load(cfg)
bot = telebot.TeleBot(config['token'])
admin = config['admins']
admin_group = config['group']


def start(message):
    answer = ask.random_questions()
    bot.send_message(message.from_user.id,
                     '<b>----------------Главное меню----------------</b>\n\n'
                     '<b>Задайте вопрос, например:</b>\n\n' + answer['msg'],
                     reply_markup=keys_start.make(), parse_mode='HTML')


@bot.message_handler(commands=['start', 'faq', 'help', 'contact'])
def faq_cmd(message):
    if message.text == '/start':
        start(message)
    elif message.text == '/faq':
        menu_faq(message)
    else:
        info.run(bot, message, message.text)


@bot.callback_query_handler(func=lambda call: call.data in ['faq', 'help', 'contact'])
def menu(call):
    if call.data == 'faq':
        menu_faq(call)
    else:
        info.run(bot, call.message, call.data)


@bot.callback_query_handler(func=lambda call: call.data in ['to_start', 'sup'])
def cancel_cmd(call):
    if call.data == 'to_start':
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except Exception as exc:
            print(exc)
        start(call)
    elif call.data == 'sup':
        sup(call)


@bot.message_handler(func=lambda message: message.text == 'Отмена')
def cancel(message):
    start(message)


def menu_faq(data):
    answer = ask.random_questions()
    bot.send_message(data.from_user.id,
                     '<b>Задайте вопрос, например:</b>\n\n' + answer['msg'],
                     reply_markup=answer['kb'],
                     parse_mode='html')


@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo",
                                    "audio", "video", "document", "contact"],
                     func=lambda message: message.reply_to_message and message.chat.id == admin_group)
def support_reply_handler(message):
    try:
        support.reply(message)
    except Exception as exc:
        print(exc)


@bot.message_handler(content_types='text', func=lambda message: message.chat.id != admin_group)
def get_question(message):
    data = ask.classify_question(message.text)
    try:
        bot.send_message(message.from_user.id, data['answer'],
                         reply_markup=data['kb'],
                         parse_mode='html')
    except Exception as exc:
        print(exc)


@bot.callback_query_handler(lambda call: re.search('q_id=', call.data))
def get_answer(call):
    msg = ask.answer(int(re.sub('q_id=', '', call.data)))
    bot.send_message(call.from_user.id, msg,
                     reply_markup=keys_sup.make(),
                     parse_mode='html')
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as exc:
        print(exc)


def sup(message):
    bot.send_message(message.from_user.id,
                     'Введите ваш номер телефона в формате +380123456789'
                     ' или нажмите "Отправить контакт"',
                     reply_markup=key_phone.make())
    bot.register_next_step_handler(message.message, get_phone)


def get_phone(message):
    if message.text == 'Отмена':
        bot.clear_step_handler(message)
        bot.send_message(message.chat.id,
                         'Регистрация заявки отменена!',
                         reply_markup=key_remove.make())
        start(message)
    else:
        phone_number = phone.get(message)
        is_valid = phone.check(phone_number)
        if is_valid and len(list(phone_number)) == 13:
            bot.send_message(message.from_user.id,
                             'Коротко опишите Ваш запрос',
                             reply_markup=key_cancel.make())
            bot.register_next_step_handler(message, register, phone_number)
        else:
            bot.send_message(message.from_user.id,
                             'Номер введен некорректно! '
                             'Введите в формате +380123456789 или нажмите "Отправить контакт"',
                             reply_markup=key_remove.make())
            bot.register_next_step_handler(message, get_phone)


def register(message, phone_number):
    if message.text == 'Отмена':
        bot.clear_step_handler(message)
        bot.send_message(message.chat.id,
                         'Регистрация заявки отменена!',
                         reply_markup=key_remove.make())
        start(message)
    else:
        task = f'#TASK{message.chat.id}_{message.message_id}'
        bot.forward_message(admin_group,
                            message.chat.id,
                            message.message_id,
                            disable_notification=True)
        bot.send_message(admin_group,
                         f'{task}\n{phone_number}',
                         reply_markup=key_reply.make(),
                         disable_notification=True)
        bot.send_message(message.from_user.id,
                         f'{task}\nЗарегистрирована в системе поддержки',
                         reply_markup=key_remove.make())


if __name__ == '__main__':
    print('bot started!\npolling..')
    while True:
        try:
            bot.polling()
        except Exception as e:
            time.sleep(60)
            print(str(e))
