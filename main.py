import time
import os
import random

import telebot

from button import *
from config import Config
from database import *
from checks import *

token = Config.token

bot = telebot.TeleBot(token=token)


conn = get_db_connection()
cur = conn.cursor()

PHOTOS_DIR = 'photos'
check_path(PHOTOS_DIR)


cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    last_message INTEGER,
    send_text_status INTEGER,
    send_text TEXT, 
    send_photo_status INTEGER,
    send_photo TEXT,
    ready_to_send INTEGER
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY,
    request_id INTEGER,
    user_id INTEGER,
    request_text TEXT,
    request_photo
)
''')

conn.commit()
conn.close()


@bot.message_handler(commands=['start'])
def send_welcome(message):

    add_user(message.chat.id)

    markup = start_menu_button()
    last_message = bot.send_message(message.chat.id, "Выберете действие!", reply_markup=markup)

    set_user_data(message.chat.id, 'last_message', last_message.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    last_message = get_user_data(call.message.chat.id, 'last_message')

    if call.data == "contact_admin":
        markup = send_contact_button()

        bot.answer_callback_query(call.id, text="Перевожу вас к админу")

        mess = bot.edit_message_text(message_id=last_message, chat_id=chat_id,
                                     text='Выберете формат обращение', reply_markup=markup)
        set_user_data(chat_id, 'last_message', mess.id)

    elif call.data == 'back_menu':
        markup = start_menu_button()

        bot.answer_callback_query(call.id, text="Возвращаюсь обратно")

        mess = bot.edit_message_text(message_id=last_message, chat_id=chat_id,
                                     text="Выберете действие!", reply_markup=markup)
        set_user_data(chat_id, 'last_message', mess.id)

    elif call.data == 'send_text':

        bot.answer_callback_query(call.id, text="Жду ваш текст")

        set_user_data(chat_id, 'send_text_status', 1)
        bot.send_message(chat_id, 'Отправьте текст сообщением 📑')

    elif call.data == 'send_photo':

        bot.answer_callback_query(call.id, text="Жду ваше фото")

        set_user_data(chat_id, 'send_photo_status', 1)
        bot.send_message(chat_id, 'Отправьте фото следующим сообщением 🖼')


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.chat.id

    if get_user_data(user_id, 'send_photo_status'):
        # сохранение файла из чата
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # генерация случайного 8-значного значения для названия фотографии
        num = ''.join(random.choices('0123456789', k=8))

        set_user_data(user_id, 'send_photo', num)

        filename = f"{num}.jpg"

        # сборка пути сохранения photos/user_id/файл
        path_dir = f'{PHOTOS_DIR}/{user_id}'

        check_path(path_dir)

        file_path = os.path.join(path_dir, filename)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"Фото сохранено!")

        set_user_data(user_id, 'send_photo_status', 0)

        time.sleep(2)

        for i in range(-1, 2):
            bot.delete_message(message.chat.id, message_id=message.id + i)


@bot.message_handler()
def send_question(message):
    chat_id = message.chat.id
    if len(message.text) > 1 and get_user_data(message.chat.id, 'send_text_status'):
        text = message.text

        set_user_data(chat_id, 'send_text', text)
        set_user_data(chat_id, 'send_text_status', 0)

        bot.reply_to(message, 'Сообщение принято!')
        time.sleep(1)

        for i in range(-1, 2):
            bot.delete_message(message.chat.id, message_id=message.id + i)


bot.polling(none_stop=True)


# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         print(f"Ошибка: {e}. Перезапуск через 5 секунд...")
#         time.sleep(5)
