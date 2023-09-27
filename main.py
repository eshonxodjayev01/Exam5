import os
from dotenv import load_dotenv
import telebot
from telebot import types
from random import shuffle
import django
django.setup()
from question.models import Question
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_bot.settings")
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')


bot = telebot.TeleBot(BOT_TOKEN)
answers = []
questions = []
# '3-4-5'
def data_cell():
    db = Question.objects.all()
    question: Question

    for question in db:
        questions.append(question.question)
        answers.append(question.answer.split('-'))
        print(question.question,question.answer)
# print(db)
# answers = [
#     ("3", "4", "5"),
#     ("0.2", "0.9", "-1"),
#     ("21", "34", "10"),
#     ("5", "0", "1"),
#     ("56", "-12", "54"),
#     ("7", "12", "13"),
# ]
# questions = [
#     "1 + 2 = ?",
#     "2 / 10 = ?",
#     "14 / 2 * 3 = ?",
#     "2 + 3 = ?",
#     "7 * 8 = ?",
#     "9 + 1 - 3 = ?",
# ]

# def data_cell():
#     db = Question.objects.all()
#     question: Question
#     for question in db:
#         questions.append(question.question)
#         answers.append(question.answer.split('-'))
#
#     print(question.question, question.answer)
#
#
#
#
#
#
count = 0


def makekeyboard(question_id: int):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for answer_id, answer in enumerate(answers[question_id]):
        buttons.append(types.InlineKeyboardButton(text=answer, callback_data=f"{question_id}_{answer_id}"))
    shuffle(buttons)
    for button in buttons:
        markup.add(button)
    return markup


@bot.message_handler(commands=['test'])
def handle_test(msg: types.Message):
    data_cell()
    bot.send_message(chat_id=msg.chat.id,
                     text=questions[0],
                     reply_markup=makekeyboard(0),
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(cb: types.CallbackQuery):
    global count
    global answers
    global questions
    question_id, answer_id = cb.data.split("_")

    if int(answer_id) == 0:
        count += 1
    if len(questions) > int(question_id) + 1:
        print(cb.data)
        bot.edit_message_text(chat_id=cb.message.chat.id, message_id=cb.message.message_id,text=questions[int(question_id) + 1], reply_markup=makekeyboard(int(question_id) + 1))
    else:
        bot.send_message(chat_id=cb.message.chat.id,text=f"Qoyil siz {len(questions)} ta savoldan, {count} ta savol toptiz!!!..")
        count = 0
        questions = []
        answers = []

# @bot.message_handler(content_types=["document"])
# def echo_all(message: types.Message):
#     bot.forward_message(GROUP_ID, message.chat.id, message.id)
#     bot.send_message(message.chat.id, "Tekshirish uchun file jo'natildi!!..")

bot.infinity_polling()