from fuzzywuzzy import fuzz
import pymorphy2
import random
from telebot import types
import sqlite3
import re


morph = pymorphy2.MorphAnalyzer()


def classify_question(text):
    questions = load()
    msg = ''
    kb = types.InlineKeyboardMarkup(row_width=3)
    row = list()

    text = ' '.join(morph.parse(word)[0].normal_form for word in text.split())
    scores = list()

    for question in questions:
        norm_question = ' '.join(morph.parse(word)[0].normal_form for word in question.split())
        current = fuzz.WRatio(
            norm_question.lower(),
            text.lower()) + fuzz.token_sort_ratio(
            norm_question.lower(),
            text.lower()
        )
        scores.append(current)

    # получение ответа
    for i in range(3):
        question = questions[scores.index(max(scores))]
        # answer += question + '\n\n' + faq[questions[scores.index(max(scores))]] + '\n\n'
        q_id = qid(question)
        row.append(types.InlineKeyboardButton(text=str(i + 1),
                                              callback_data=f'q_id={q_id}'))
        msg += f'{i+1}. {question}\n\n'
        questions.pop(scores.index(max(scores)))
        scores.pop(scores.index(max(scores)))
    kb.add(*row)
    return {'answer': msg, 'kb': kb}


def random_questions():
    questions = load()
    msg = ''
    kb = types.InlineKeyboardMarkup(row_width=3)
    row = list()
    for i in range(3):
        r = random.randint(0, len(questions)-1)
        print(r)
        msg += f'{i+1}. {questions[r]}\n\n'
        q_id = qid(questions[r])
        row.append(types.InlineKeyboardButton(text=str(i + 1),
                                              callback_data=f'q_id={q_id}'))
    kb.add(*row)
    return {'msg': msg, 'kb': kb}


def load():
    conn = sqlite3.connect('info/faq.db')
    cursor = conn.cursor()
    sql = "SELECT q FROM faq"
    rows = cursor.execute(sql).fetchall()
    questions = ', '.join(re.sub(r"\('", '', re.sub(r"',\)", '', str(r))) for r in rows).split(', ')
    conn.close()
    return questions


def qid(question):
    conn = sqlite3.connect('info/faq.db')
    cursor = conn.cursor()
    sql = f"SELECT n FROM faq WHERE q='{question}'"
    rows = cursor.execute(sql).fetchall()
    q_id = re.sub(r"\(", '', re.sub(r",\)", '', str(rows[0])))
    conn.close()
    return q_id


def answer(q_id):
    conn = sqlite3.connect('info/faq.db')
    cursor = conn.cursor()
    sql = f"SELECT q FROM faq WHERE n={q_id}"
    rows = cursor.execute(sql).fetchall()
    q = re.sub(r"\('", '', re.sub(r"',\)", '', str(rows[0])))
    sql = f"SELECT a FROM faq WHERE n={q_id}"
    rows = cursor.execute(sql).fetchall()
    a = re.sub(r"\('", '', re.sub(r"',\)", '', str(rows[0])))
    conn.close()
    msg = f'<b>{q}</b>\n\n{a}'
    return msg
