from telebot import types


def start_menu_button():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Обратиться к админу 👤", callback_data="contact_admin")
    btn2 = types.InlineKeyboardButton(text="Стать админом 🔼", callback_data="become_admin")
    markup.add(btn1)
    markup.add(btn2)

    return markup


def send_contact_button():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Фотка 📷', callback_data="send_photo")
    btn2 = types.InlineKeyboardButton(text='Текст 📔', callback_data="send_text")
    btn3 = types.InlineKeyboardButton(text='Отправить 📬', callback_data='send')
    btn4 = types.InlineKeyboardButton(text='Назад ◀️', callback_data='back_menu')

    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)

    return markup
