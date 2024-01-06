import re
import datetime
import time

from antiflood import rate_limit
from aiogram import types, Dispatcher

from create import bot, mute_db


mut_sec = 0


@rate_limit(limit=2)
async def mute_user(message: types.Message):
    global mut_sec
    command_pattern = r"/mute\s*(\d+)\s*([a-zA-Zа-яА-Я]+)"
    match = re.match(command_pattern, message.text)

    mut_units = {
        "сек": ["сек", "секунд", "секунды", "s", "second", "seconds", "с"],
        "хв": ["мин", "минут", "минуты", "m", "minute", "minutes", "м"],
        "год": ["час", "часов", "ч", "h", "hour", "hours", "часиков"],
        "нед": ["неделя", "недель", "н", "w", "week", "weeks"]
    }

    if match:
        duration = int(match.group(1))
        unit = match.group(2).lower()

        selected_unit = None
        for key, aliases in mut_units.items():
            if unit.lower() in [alias.lower() for alias in aliases]:
                selected_unit = key
                break

        if selected_unit:
            mut_sec = duration
            if selected_unit == "хв":
                mut_sec *= 60
            elif selected_unit == "год":
                mut_sec *= 3600
            elif selected_unit == "нед":
                mut_sec *= 604800

        chat_id = message.chat.id

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id

            until_date = int(time.time()) + mut_sec

            mute_db.add_mute(user_id, until_date)

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

            await bot.restrict_chat_member(chat_id, user_id, permissions, until_date=until_date)

            until_date_str = datetime.datetime.fromtimestamp(until_date).strftime('%m-%d | %H:%M')

            await message.reply(f"в муте до {until_date_str}")

        else:
            await message.reply('Команда должна быть ответом на сообщение.')
    else:
        await message.reply(
            "Неправильный формат.")


@rate_limit(limit=2)
async def unmute_user(message: types.Message):

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
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

        await bot.restrict_chat_member(chat_id, user_id, permissions)
        await message.reply("Пользователь больше не в муте")
    else:
        await message.reply("Команда должна быть ответом на сообщение")


def register_mute(dp: Dispatcher):
    dp.register_message_handler(mute_user, is_admin=True, commands=['mute'])
    dp.register_message_handler(unmute_user, is_admin=True, text=['/unmute', 'говори'])
