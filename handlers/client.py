import random
import re
import html

from aiogram import types, Dispatcher
from antiflood import rate_limit

from keyboard import keyboard_client
from create import (db_rules, db_group, db_pred_user, db_pred, db_add_user,
                    db_add_day, db_bad_day, db_add_bad, db_words, welcome_db)

from text.bad_words import mat
from text.client_text import who_text, danet_text


@rate_limit(limit=2)
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(
            """
           <b>Привет! 👋</b>\n\n
Я <i>чат-менеджер</i>, создан для управления чатами.
Моя цель - помогать вам легко и удобно управлять общением в чатах. 🚀\n\n
Чтобы <i>добавить меня в чат</i>, просто нажмите на кнопку ниже.
 Я готов помочь вам улучшить опыт общения ваших участников!⬇️\n\n
 """,
            reply_markup=keyboard_client.button_add_start(), parse_mode="HTML")
    elif message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        await message.answer("""
<b>Я чат-менеджер</b> 🤖. Для настройки введите команду \n<code>/config</code>.
""", parse_mode="HTML")


@rate_limit(limit=2)
async def comand_list(message: types.Message):
    await message.answer("https://teletype.in/@dobrychek/q3QWyxkYax-", disable_web_page_preview=True)


@rate_limit(limit=2)
async def delete_rules(message: types.Message):
    if db_rules.delete_rules(message.chat.id):
        await message.answer("Правила успешно удалены")
    else:
        await message.answer("""
<b>❗ Правила не установлены</b>. Для настройки введите команду <code>/config</code> ⚙️.""", parse_mode='HTML')


@rate_limit(limit=2)
async def delete_welcome(message: types.Message):
    if welcome_db.delete_rules(message.chat.id):
        await message.answer("Приветствие успешно удалено")
    else:
        await message.answer("""
<b>❗ Приветствие не установлено</b>. Для настройки введите команду <code>/config</code> ⚙️.""", parse_mode='HTML')


@rate_limit(limit=2)
async def rules(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        if db_rules.get_rules(message.chat.id) == 'Правила не установлены':
            await message.reply("""
<b>❗ Правила не установлены</b>. Для настройки введите команду <code>/config</code> ⚙️.
""", parse_mode='HTML')
        else:
            await message.answer(f'<b>Правила чата:</b> 📜\n\n{db_rules.get_rules(message.chat.id)}',
                                 parse_mode='HTML')


@rate_limit(limit=2)
async def config(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        await message.answer("<b>Настройки бота ⚙️</b>",
                             reply_markup=keyboard_client.setting_menu(), parse_mode='HTML')


@rate_limit(limit=2)
async def top_boltunov(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        da = db_words.get_group_messages(message.chat.id)
        da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

        messages = []
        for user_id, name, message_count in da_sorted[:30]:
            if db_words.get_group_messages(user_id) is not None:
                name_escaped = html.escape(name)
                messages.append(f"<i>{name_escaped}</i> - <b>{message_count}</b>")

        group_message = "\n".join(messages)
        total_message_count = db_words.get_total_message_count_for_group(message.chat.id)
        total_message_count_escaped = html.escape(str(total_message_count))
        await message.answer(
            f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_message_count_escaped}</b>",
            parse_mode='HTML')


@rate_limit(limit=2)
async def top_eblanov(message):
    if message.chat.type != types.ChatType.PRIVATE:
        da = db_pred_user.get_group_messages_pred(message.chat.id)
        da_sorted = sorted(da, key=lambda item: item[2], reverse=True)
        messages = [f"<a href='tg://user?id={user_id}'>{name}</a> - {message_count}/{db_pred.get_default_pred_value()}"
                    for
                    user_id, name, message_count in
                    da_sorted if
                    db_pred_user.get_group_messages_pred(user_id) is not None]
        group_message = "\n".join(messages)
        return group_message


@rate_limit(limit=2)
async def danet(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        if message.text.startswith(".данет"):
            user_id, name = db_group.get_random_user_with_name_from_user_messages_table(message.from_user.id)
            await message.answer(
                f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> "
                f"{random.choice(danet_text(user_id, name))}",
                parse_mode="HTML")


@rate_limit(limit=2)
async def who(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        words_after_bot_kto = message.text[7:]
        user_id, name = db_group.random_user_with_name_from_user_messages_table()
        await message.answer(
            f"{random.choice(who_text(name, user_id, words_after_bot_kto))}",
            parse_mode="HTML")


@rate_limit(limit=2)
async def infa(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        await message.answer(
            f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            f" Судя по данным, вероятность составляет {random.randint(0, 100)}%.",
            parse_mode="HTML")


async def user_all(message: types.Message):
    if message.text:
        db_add_user.add_user_id(message.from_user.id, message.from_user.full_name)
        if message.chat.type != types.ChatType.PRIVATE:
            user_id = message.from_user.id
            db_words.add_or_update_user(user_id, message.from_user.first_name, message.chat.id)
            db_add_day.add_new_message(message.from_user.id, message.from_user.full_name, message.chat.id)
            for i in mat:
                if i.lower() in message.text.lower():
                    db_add_bad.add_or_update_user(message.from_user.id, message.from_user.full_name, message.chat.id)
                    db_bad_day.add_new_message(message.from_user.id, message.from_user.full_name, message.chat.id)


async def send_top_messages(message, get_data_func, db_instance):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = get_data_func(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0

            for user_id, name, message_count in da_sorted[:30]:
                if get_data_func(user_id) is not None:
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception as ex:
        await message.answer("Список пуст")
        print(ex)


@rate_limit(limit=2)
async def top_pizdabol(message: types.Message):
    await send_top_messages(message, db_add_bad.get_group_messages, db_add_bad)


@rate_limit(limit=2)
async def top_pizdabol_day(message: types.Message):
    await send_top_messages(message, db_bad_day.get_top_messages_last_24_hours, db_bad_day)


@rate_limit(limit=2)
async def top_pizdabol_week(message: types.Message):
    await send_top_messages(message, db_bad_day.get_top_messages_last_week, db_bad_day)


@rate_limit(limit=2)
async def top_pizdabol_month(message: types.Message):
    await send_top_messages(message, db_bad_day.get_top_messages_last_month, db_bad_day)


@rate_limit(limit=2)
async def top_group_day(message: types.Message):
    await send_top_messages(message, db_add_day.get_top_messages_last_24_hours, db_add_day)


@rate_limit(limit=2)
async def top_group_week(message: types.Message):
    await send_top_messages(message, db_add_day.get_top_messages_last_week, db_add_day)


@rate_limit(limit=2)
async def top_group_month(message: types.Message):
    await send_top_messages(message, db_add_day.get_top_messages_last_month, db_add_day)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(config, is_admin=True, commands=['config'])
    dp.register_message_handler(danet, regexp=re.compile(r'^\.данет'))
    dp.register_message_handler(who, lambda message: message.text.lower().startswith("бот кто"))
    dp.register_message_handler(infa, lambda message: message.text.lower().startswith("бот инфа"))
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(rules, commands=['rules'])
    dp.register_message_handler(delete_rules, text=['.удалить правила'])
    dp.register_message_handler(delete_welcome, text=['.удалить прив'])
    dp.register_message_handler(comand_list, commands=['commands'])


def register_top_commands(dp: Dispatcher):
    dp.register_message_handler(top_boltunov, text=['Болтуны', 'болтуны', 'Топ', 'топ'])
    dp.register_message_handler(top_group_day, text=['Болтуны день', 'болтуны день', 'Топ день', 'топ день'])
    dp.register_message_handler(top_group_week, text=['Болтуны неделя', 'болтуны неделя', 'Топ неделя', 'топ неделя'])
    dp.register_message_handler(top_group_month, text=['Болтуны месяц', 'болтуны месяц', 'Топ месяц', 'топ месяц'])
    dp.register_message_handler(top_pizdabol, text=['пиздаболы', 'Пиздаболы', 'Быдло', 'быдло'])
    dp.register_message_handler(top_pizdabol_day, text=['Пиздабол день', 'пиздабол день', 'Быдло день', 'быдло день'])
    dp.register_message_handler(top_pizdabol_week,
                                text=['Пиздабол неделя', 'пиздабол неделя', 'быдло неделя', 'Быдло неделя'])
    dp.register_message_handler(top_pizdabol_month,
                                text=['Пиздабол месяц', 'пиздабол месяц', 'Быдло месяц', 'быдло месяц'])


def register_user_all(dp: Dispatcher):
    dp.register_message_handler(user_all)
