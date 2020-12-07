from keyboards import kb
import re


def run(bot, message, data):
    filename = re.sub('/', '', data)
    with open(f"info/{filename}.txt", "r", encoding='UTF-8') as txt:
        bot.send_message(message.chat.id,
                         "".join(txt.read()),
                         reply_markup=kb.to_start(),
                         parse_mode='HTML')
