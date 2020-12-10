from bot import bot, dump_data
import re


def reply(message):
    if re.search(r'^#TASK', message.reply_to_message.text):
        reply_to_text = message.reply_to_message.text
        task_id = re.sub('#TASK', '', reply_to_text)
        chat_id = int(re.search(r'^\d+', task_id).group())
        text = re.sub(r'\+\d+$', '', reply_to_text)
        msg = bot.send_message(chat_id, f'Ответ на заявку:\n{text}')
        bot.forward_message(chat_id, message.chat.id, message.message_id)
        bot.reply_to(message, 'Ответ успешно доставлен')
        dump_data(message.from_user, msg.chat, message.text, ptype='TASK REPLY')
    else:
        bot.reply_to(message, 'Ответ необходимо дать на сообщение с номером заявки!')
