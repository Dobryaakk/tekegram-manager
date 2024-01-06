from aiogram import types, Dispatcher
from create import welcome_db


async def new_chat_members_handler(message: types.Message):
    new_members = message.new_chat_members
    if welcome_db.get_welcome(message.chat.id) == "Приветствие не установлено":
        return
    welcome_text = welcome_db.get_welcome(message.chat.id)
    for member in new_members:
        await message.reply(welcome_text)


def register_chat_member(dp: Dispatcher):
    dp.register_message_handler(new_chat_members_handler, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
