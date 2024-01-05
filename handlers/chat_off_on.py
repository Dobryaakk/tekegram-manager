from aiogram import types, Dispatcher
from create import bot
from antiflood import rate_limit


@rate_limit(limit=2)
async def offchat(message: types.Message):
    chat_id = message.chat.id

    permissions = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
    )

    await bot.set_chat_permissions(chat_id, permissions)
    await message.reply("чат доступен только админам")


@rate_limit(limit=2)
async def onchat(message: types.Message):
    chat_id = message.chat.id

    permissions = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True,
    )

    await bot.set_chat_permissions(chat_id, permissions)
    await message.reply("чат доступен всем")


def register_chat_off_on(dp: Dispatcher):
    dp.register_message_handler(offchat, text=["-чат"])
    dp.register_message_handler(onchat, text=["+чат"])
