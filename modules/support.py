from bot import bot
import re


def reply(message):
    reply_to_text = message.reply_to_message.text
    task_id = re.sub('#TASK', '', reply_to_text)
    chat_id = int(re.search(r'^\d+', task_id).group())
    text = re.sub(r'\+\d+$', '', reply_to_text)
    bot.send_message(chat_id, f'Ответ на заявку:\n{text}')
    bot.forward_message(chat_id, message.chat.id, message.message_id)