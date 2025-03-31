import sqlite3


def get_db_connection():
    """Функция для подключения к базе данных"""
    return sqlite3.connect('users_pr.db', check_same_thread=False)


def add_user(user_id, last_message=0, send_text_status=0,
             send_text='', send_photo_status=0, send_photo='', ready_to_send=0):
    """Добавление нового пользователя в базу данных"""
    conn = get_db_connection()
    cur = conn.cursor()
    if not user_exist(user_id):
        cur.execute('INSERT INTO users (user_id, last_message, send_text_status, '
                    'send_text, send_photo_status, send_photo, ready_to_send) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (user_id, last_message, send_text_status, send_text, send_photo_status, send_photo, ready_to_send,))
    conn.commit()
    conn.close()


def user_exist(user_id):
    """Проверка есть ли пользователь с определенным id в базе данных"""
    connect = get_db_connection()
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    connect.close()
    return count


def get_user_data(user_id, paste):
    """Получение значения ячейки у определенного пользователя, paste - название ячейки"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT {paste} FROM users WHERE user_id = ?', (user_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return 0


def set_user_data(user_id, paste, param):
    """Обновление значения ячейки у существующего пользователя
        paste - название ячейки, param - устанавливаемое значение"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET {paste} = ? WHERE user_id = ?', (param, user_id,))
    conn.commit()
    conn.close()


def get_request_data(request_id, paste):
    """Получение данных запроса, paste - название ячейки"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT {paste} FROM users WHERE request_id = ?', (request_id,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return 0


def set_request_data(request_id, paste, param):
    """Обновление данных запроса, paste - название ячейки, param - устанавливаемые данные"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET {paste} = ? WHERE request_id = ?', (param, request_id,))
    conn.commit()
    conn.close()
