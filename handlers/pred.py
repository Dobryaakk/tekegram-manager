from aiogram import types, Dispatcher

from create import db_pred, db_pred_user, db_pred_dead
from create import bot
from antiflood import rate_limit


@rate_limit(limit=2)
async def pred(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE and message.reply_to_message is not None:
        db_pred_user.add_or_update_user(message.reply_to_message.from_user.id,
                                        message.reply_to_message.from_user.full_name, message.chat.id)
        k = db_pred_user.get_user_pred_count(message.reply_to_message.from_user.id, message.chat.id)
        b = db_pred.get_default_pred_value()
        if k < b:
            await message.answer(
                f'предупреждение добавлено {k}/{b}')
        elif k == b:
            db_pred_user.remove_user_entry(message.reply_to_message.from_user.id, message.chat.id)
            if db_pred_dead.get_default_dead_text() == 'bun':
                chat_id = message.chat.id
                user_id = message.reply_to_message.from_user.id
                await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            else:
                chat_id = message.chat.id
                user_id = message.reply_to_message.from_user.id
                await bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
                await message.answer(f'Пользователь получил максимальное количетсво предупреждений {k}/{b}')


def register_pred(dp: Dispatcher):
    dp.register_message_handler(pred, commands=['pred'])
