import telebot as tb
from telebot import types

import requests
from bs4 import BeautifulSoup


bot = tb.TeleBot('ваш token')


@bot.message_handler(commands=['start', 'info'])
def start_info(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    butt1 = types.KeyboardButton("Пн")
    butt2 = types.KeyboardButton("Вт")
    butt3 = types.KeyboardButton("Ср")
    butt4 = types.KeyboardButton("Чт")
    butt5 = types.KeyboardButton("Птн")
    butt6 = types.KeyboardButton("Сб")
    butt7 = types.KeyboardButton("Вс")
    menu.add(butt1, butt2, butt3, butt4, butt5, butt6, butt7)
    bot.send_message(message.chat.id, "Могу показать расписание, выберите день:", \
                    reply_markup=menu)


@bot.message_handler(commands=['tr'])
def word_catch(message):
    send = bot.send_message(message.chat.id, 'Введите слово: ')
    bot.register_next_step_handler(send, translate)

def translate(message):
    url = 'https://wooordhunt.ru/word/' + message.text
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    try:
        # для перевода с английского на русский
        data = soup.find('span', {'class': 't_inline_en'})
        if data == None:
            # для перевода с русского на английский
            data = soup.find('p', {'class': 't_inline'})
        tr = 'варианты перевода: {}'.format(data.get_text())
    except:
        tr = 'The word "{}" is not found'.format(message.text)
    bot.send_message(message.chat.id, tr)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.chat.type == 'private':
        if message.text == "Пн":
            bot.send_message(message.chat.id, "1. Английский\n2. Алгебра\n3. Физика")
        elif message.text == "Вт":
            bot.send_message(message.chat.id, "<тут будет расписание на вторник>")
        elif message.text == "Ср":
            bot.send_message(message.chat.id, "<тут будет расписание на среду>")
        elif message.text == "Чт":
            bot.send_message(message.chat.id, "<тут будет расписание на четверг>")
        elif message.text == "Птн":
            bot.send_message(message.chat.id, "<тут будет расписание на пятницу>")
        elif message.text == "Сб":
            bot.send_message(message.chat.id, "<тут будет расписание на субботу>")
        elif message.text == "Вс":
            bot.send_message(message.chat.id, "<тут будет расписание на воскресение>")
        else:
            # создаём клавиатуру с кнопками "да", "нет"
            inline = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton('yes', callback_data='yes')
            button2 = types.InlineKeyboardButton('no', callback_data='no')

            inline.add(button1, button2)

            bot.send_message(message.chat.id, 'Узнать время занятий?', reply_markup=inline)



@bot.message_handler(content_types=['documents', 'voice'])
def get_text(message):
    bot.send_message(message.chat.id, "Не работаю с такими типами сообщений")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, '1. 8:00 - 8:45\n2. 9:00 - 9:45\n...')
    else:
        bot.send_message(call.message.chat.id, 'ладно, не покажу')


bot.polling(none_stop=True)