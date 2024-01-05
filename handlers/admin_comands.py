# from aiogram import types, Dispatcher
# from my_poject_moder.database.db import Database_add_admin
# from my_poject_moder.config.config import *
#
# db_add_admin = Database_add_admin('bd.db')
#
#
# async def staff(message: types.Message):
#     admins = db_add_admin.staff()
#     message_text = "список админов\n"
#     for admin_name in admins:
#         admin_link = f'<a href="https://t.me/{admin_name}">{admin_name}</a>'
#         message_text += admin_link + "\n"
#
#     await message.answer(message_text, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
#
#
# async def add_admin(message: types.Message):
#     if message.from_user.id == OWNER_ID and message.reply_to_message:
#         if not db_add_admin.user_admin_exists(message.reply_to_message.from_user.id):
#             db_add_admin.add_admin_user(message.reply_to_message.from_user.id,
#                                         message.reply_to_message.from_user.username)
#             reply_message = message.reply_to_message.from_user.username
#             await message.answer(f"админ @{reply_message} добавлен")
#
#
# async def admin(message: types.Message):
#     user_to_remove = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
#     if db_add_admin.is_admin(user_to_remove):
#         db_add_admin.remove_admin(user_to_remove)
#         await message.answer(
#             f"пользователь @{user_to_remove} исключен с должности админа")
#     else:
#         await message.answer("пользователь не являеться админом")
#
#
# def register_admin_comands(dp: Dispatcher):
#     dp.register_message_handler(staff, text=['/staff', '!админ лист', '.админ лист'])
#     dp.register_message_handler(add_admin, commands=['up'])
#     dp.register_message_handler(admin, text=['!разжаловать', '.разжаловать'])
