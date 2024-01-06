words_setting = {  # тут ты просто собираешь все фразы с файла settings и вставлянш в список ниже
    "RU": [
        '🔥 Введи текст',
        '🔎 еще фраза',
        ' и тут чето на русс',
        ' и злдесь',
        '👤 и кароче все на русс',
        'Введите название трека',
        'Выберете платформу для поиска',
        'Выберите язык',
    ],

    "EN": [  # вот тут те же фразы c settings но на англ яз
        '🔥 Top',
        '🔎 Search',
        'ℹ Information',
        '🌏 Language',
        '👤 My Profile',
        'Enter a track name',
        'Choose a platform to search for',
        'Choose language'
    ]
}

words_keyboard = {  # тут ты просто собираешь все фразы с файла keyboard и вставлянш в список ниже
    "RU": [
        '🔥 Введи текст',
        ' назад',
        ' вперед',
        ' раком',
        '👤 боком',
        ' и тд',
        'Выберете платформу для поиска',
        'Выберите язык',
    ],

    "EN": [  # вот тут те же фразы c keyboard но на англ яз
        '🔥 Top',
        '🔎 Search',
        'ℹ Information',
        '🌏 Language',
        '👤 My Profile',
        'Enter a track name',
        'Choose a platform to search for',
        'Choose language'
    ]
}
''' И ВОТ ТАК СОЗДАЕШЬ СЛОВАРИ ДЛЯ КАЖДОГО ФАЙЛА И В КАЖДОМ ТАКОМ СЛОВАРЕ БУДУТ ФРАЗЫ С КАКОГОТО ФАЙЛА'''
'''А ПОТОМ Я ПРОСТО БУДУ ОТБРАЩАТЬСЯ К СЛОВАРЮ ПО ЯЗЫКУ И БУДУ ДОСТАВАТЬ ФРАЗЫ'''

# async def profile(message: types.Message):
#     user_id, name, time = db_add_user.get_random_user_with_name_from_table()
#     telegram_user_id = message.from_user.id
#     user_profile_photos = await bot.get_user_profile_photos(user_id=telegram_user_id)
#
#     if user_profile_photos.total_count > 0:
#         photo = user_profile_photos.photos[0][-1]
#         file_id = photo.file_id
#
#         await bot.send_photo(message.chat.id, photo=file_id,
#                         caption=f"Профииль <a href='tg://user?id={telegram_user_id}'>{message.from_user.full_name}</a>\n"
#                          f"Первое появление {time[:10]}"
#                          f"Стать: {}", parse_mode='HTML')


import datetime
import sqlite3
import time







# class Database_language:
#     def __init__(self, db_file):
#         self.conn = sqlite3.connect(db_file)
#         self.cur = self.conn.cursor()
#         self.create_table()
#
#     def create_table(self):
#         with self.conn:
#             self.cur.execute("""
#             CREATE TABLE IF NOT EXISTS language (
#                        user_id INTEGER,
#                        lang TEXT
#                        )
#                """)
#
#     def add_user_lang(self, user_id, lang):
#         with self.conn:
#             self.cur.execute("INSERT INTO language VALUES (?, ?)", (user_id, lang))


# class Database_add_admin:
#     def __init__(self, db_file):
#         self.conn = sqlite3.connect(db_file)
#         self.cur = self.conn.cursor()
#         self.user_admin()
#
#     def user_admin(self):
#         with self.conn:
#             self.cur.execute("""
#                         CREATE TABLE IF NOT EXISTS user_admin (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             user_id INTEGER UNIQUE,
#                             name TEXT
#                         )
#                     """)
#
#     def user_admin_exists(self, user_id):
#         with self.conn:
#             result = self.cur.execute("SELECT * FROM user_admin WHERE user_id = ?", (user_id,)).fetchall()
#             return bool(len(result))
#
#     def add_admin_user(self, user_id, full_name):
#         if not self.user_admin_exists(user_id):
#             with self.conn:
#                 self.cur.execute("INSERT INTO user_admin (user_id, name) VALUES (?, ?)", (user_id, full_name,))
#                 self.conn.commit()
#
#     def staff(self):
#         with self.conn:
#             res_adm = self.cur.execute("SELECT name FROM user_admin").fetchall()
#             return [name[0] for name in res_adm]
#
#     def is_admin(self, user_id_or_username):
#         with self.conn:
#             result = self.cur.execute("SELECT * FROM user_admin WHERE user_id = ? OR name = ?",
#                                       (user_id_or_username, user_id_or_username)).fetchall()
#             return bool(len(result))
#
#     def remove_admin(self, user_id_or_username):
#         with self.conn:
#             self.cur.execute("DELETE FROM user_admin WHERE user_id = ? OR name = ?",
#                              (user_id_or_username, user_id_or_username))
#             self.conn.commit()
#
