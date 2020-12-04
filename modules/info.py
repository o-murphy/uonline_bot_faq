from keyboards import key_to_start
import re


def run(bot, message, data):
    filename = re.sub('/', '', data)
    with open(f"info/{filename}.txt", "r", encoding='UTF-8') as txt:
        bot.send_message(message.chat.id,
                         "".join(txt.read()),
                         reply_markup=key_to_start.make(),
                         parse_mode='HTML')
