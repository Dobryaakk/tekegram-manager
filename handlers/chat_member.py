from aiogram import types, Dispatcher
from database.db import Database_welcome

db_welcome = Database_welcome('bd.db')


async def new_chat_members_handler(message: types.Message):
    new_members = message.new_chat_members
    if db_welcome.get_welcome(message.chat.id) == "Приветствие не установлено":
        return
    welcome_text = db_welcome.get_welcome(message.chat.id)
    for member in new_members:
        await message.reply(welcome_text)


async def delete_members_handler(message: types.Message):
    await message.reply('нуи пиздуй')


def register_chat_member(dp: Dispatcher):
    dp.register_message_handler(new_chat_members_handler, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(delete_members_handler, content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
