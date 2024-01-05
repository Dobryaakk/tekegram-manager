import random
import re
import asyncio

from aiogram import types, Dispatcher
from antiflood import rate_limit
from aiogram.types import ParseMode

from database.db import Database_rules, Database_group, Database_group_words, Database_pred_user, \
    Database_user_all, Database_group_bad_words, Database_group_words_day, Database_group_bad_words_day, Database_pred
from keyboard import keyboard_client

db_rules = Database_rules('bd.db')
db_group = Database_group('bd.db')
db_words = Database_group_words('bd.db')
db_pred_user = Database_pred_user('bd.db')
db_add_user = Database_user_all('bd.db')
db_add_bad = Database_group_bad_words('bd.db')
db_add_day = Database_group_words_day('bd.db')
db_bad_day = Database_group_bad_words_day('bd.db')
db_pred = Database_pred('bd.db')

pis = """ой летилы дыки гусы
налысники з маком
корова пасеця
пильмени с мясам
а ми кашу не доилы
коцб деревяни
цеп злетив з велосыпеда
баба спыть у ями
ластивки ластивки ластивки
рамашки ромашки ромашки
вышни черешни слывки
надиньте мурашци фурашку
ой летилы дыки гусы
дид бижыть з метлою
на дорози лежить купа
мишок з травою
в зуби застряла картоплына
риже батько дрова
пив мишка видра гороху
высралась корова
ластивки ластивки ластивки
рамашки ромашки ромашки
вышни черешни слывки
надиньте мурашци фурашку
ой летилы дики гусы
палатка промокла
свичка свите та не грие
собака здохла
пид дощем высохло сино
дерева трясуться
буряки позабувалы
а свыни несутся
ластивки ластивки ластивки
рамашки ромашки ромашки
вышни черешни слывки
надиньте мурашци фурашку
ой летилы дыкы гусы
тай не долетилы
банчк крышкою накрытый
а дрова згорилы
на подври баба галя
мотоцикл скраю
асфальт хороший
дальше я не знаю
"""


async def song(message: types.Message):
    for line in pis.splitlines():
        print(message.text)  # Додайте цей рядок для відлагодження
        if message.text == 'stop':  # Замініть "и" на "і" тут
            return
        await message.answer(line, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(1)



@rate_limit(limit=2)
async def dobryak(message: types.Message):
    if message.from_user.id == 1280899097:
        await message.answer("Шо хазаяин, звал?")
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEBYsVlJVj-aUd_FhREdp31BVMJlsqw3gAC6B8AAltwqUo_tyeq6zPpmzAE')
    else:
        await message.reply("Язык чуркский твой не понимаю")


@rate_limit(limit=2)
async def here(message: types.Message):
    await message.answer("А табе это ебать не должно")
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEBYsVlJVj-aUd_FhREdp31BVMJlsqw3gAC6B8AAltwqUo_tyeq6zPpmzAE')


@rate_limit(limit=2)
async def say(message: types.Message):
    if message.from_user.id == 1280899097:
        await message.answer(message.text[13:])
    else:
        await message.answer("я шо табе собака какаято шоб подчиняться табе")
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEBYsVlJVj-aUd_FhREdp31BVMJlsqw3gAC6B8AAltwqUo_tyeq6zPpmzAE')


@rate_limit(limit=2)
async def bot(message: types.Message):
    await message.answer("я вопшето мовп")
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEBYsVlJVj-aUd_FhREdp31BVMJlsqw3gAC6B8AAltwqUo_tyeq6zPpmzAE')



@rate_limit(limit=2)
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(
            """
           <b>Привет! 👋</b>\n\n
Я <i>чат-менеджер</i>, создан для управления чатами. Моя цель - помогать вам легко и удобно управлять общением в чатах. 🚀\n\n
Чтобы <i>добавить меня в чат</i>, просто нажмите на кнопку ниже. Я готов помочь вам улучшить опыт общения ваших участников!⬇️\n\n
 """,
            reply_markup=keyboard_client.button_add_start(), parse_mode="HTML")
    elif message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
        if db_group.is_group_id_present(message.chat.id) == False:
            db_group.add_group_id(message.chat.id)
            await message.answer("""
<b>Я чат-менеджер</b> 🤖. Для настройки введите команду \n<code>/config</code>.
""", parse_mode="HTML")
        await message.answer("""
<b>Я чат-менеджер</b> 🤖. Для настройки введите команду \n<code>/config</code>.
""", parse_mode="HTML")


@rate_limit(limit=2)
async def comand_list(message: types.Message):
    await message.answer("https://teletype.in/@dobrychek/q3QWyxkYax-", disable_web_page_preview=True)


@rate_limit(limit=2)
async def delete(message: types.Message):
    if db_rules.delete_rules(message.chat.id):
        await message.answer("Правила успешно удалены")
    else:
        await message.answer("""
<b>❗ Правила не установлены</b>. Для настройки введите команду <code>/config</code> ⚙️.""", parse_mode='HTML')


@rate_limit(limit=2)
async def rules(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        if db_rules.get_rules(message.chat.id) == 'Правила не установлены':
            await message.reply("""
<b>❗ Правила не установлены</b>. Для настройки введите команду <code>/config</code> ⚙️.
""", parse_mode='HTML')
        else:
            await message.answer(f'<b>Правила чата:</b> 📜\n\n{db_rules.get_rules(message.chat.id)}', parse_mode='HTML')


@rate_limit(limit=2)
async def config(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        await message.answer("<b>Настройки бота ⚙️</b>", reply_markup=keyboard_client.setting_menu(), parse_mode='HTML')


import html


@rate_limit(limit=2)
async def top_boltunov(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        da = db_words.get_group_messages(message.chat.id)
        da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

        messages = []
        # Loop through the first 30 items in da_sorted list
        for user_id, name, message_count in da_sorted[:30]:
            if db_words.get_group_messages(user_id) is not None:
                # Екрануємо спеціальні символи HTML у тексті імені користувача
                name_escaped = html.escape(name)
                messages.append(f"<i>{name_escaped}</i> - <b>{message_count}</b>")

        group_message = "\n".join(messages)
        total_message_count = db_words.get_total_message_count_for_group(message.chat.id)
        # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
        total_message_count_escaped = html.escape(str(total_message_count))
        await message.answer(
            f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_message_count_escaped}</b>",
            parse_mode='HTML')




@rate_limit(limit=2)
async def top_pizdabol(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_add_bad.get_group_messages(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_add_bad.get_group_messages(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_message_count_escaped = html.escape(str(db_add_bad.get_total_message_count_for_group(message.chat.id)))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_message_count_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")


@rate_limit(limit=2)
async def top_pizdabol_day(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_bad_day.get_top_messages_last_24_hours(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0  # Ініціалізація загальної кількості повідомлень

            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_bad_day.get_top_messages_last_24_hours(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")



@rate_limit(limit=2)
async def top_pizdabol_week(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_bad_day.get_top_messages_last_week(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0  # Ініціалізація загальної кількості повідомлень

            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_bad_day.get_top_messages_last_week(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")


@rate_limit(limit=2)
async def top_pizdabol_month(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_bad_day.get_top_messages_last_month(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0  # Ініціалізація загальної кількості повідомлень

            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_bad_day.get_top_messages_last_month(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")



@rate_limit(limit=2)
async def top_group_day(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_add_day.get_top_messages_last_24_hours(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0  # Ініціалізація загальної кількості повідомлень

            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_add_day.get_top_messages_last_24_hours(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")



@rate_limit(limit=2)
async def top_group_week(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_add_day.get_top_messages_last_week(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0  # Ініціалізація загальної кількості повідомлень

            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_add_day.get_top_messages_last_week(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")



@rate_limit(limit=2)
async def top_group_month(message: types.Message):
    try:
        if message.chat.type != types.ChatType.PRIVATE:
            da = db_add_day.get_top_messages_last_month(message.chat.id)
            da_sorted = sorted(da, key=lambda item: item[2], reverse=True)

            messages = []
            total_messages = 0  # Ініціалізація загальної кількості повідомлень

            # Loop through the first 30 items in da_sorted list
            for user_id, name, message_count in da_sorted[:30]:
                if db_add_day.get_top_messages_last_month(user_id) is not None:
                    # Екрануємо спеціальні символи HTML у тексті імені користувача та кількості повідомлень
                    name_escaped = html.escape(name)
                    message_count_escaped = html.escape(str(message_count))
                    messages.append(f"{name_escaped} - {message_count_escaped}")
                    total_messages += message_count

            group_message = "\n".join(messages)
            # Екрануємо спеціальні символи HTML у загальній кількості повідомлень
            total_messages_escaped = html.escape(str(total_messages))
            await message.answer(
                f"{group_message}\n\n<i>Всего сообщений</i> - <b>{total_messages_escaped}</b>",
                parse_mode='HTML')
    except Exception:
        await message.answer("Список пуст")



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

@rate_limit(limit=2)
async def danet(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        if message.text.startswith(".данет"):
            user_id, name = db_group.get_random_user_with_name_from_user_messages_table(message.from_user.id)
            danet = [
                '🔍 <b>Безусловно, в этом нет сомнений!</b>',
                '⚖️ <b>Да, конечно, это как дважды два пять.</b>',
                '❓ <b>Я бы сказал, что да, но не скажу.</b>',
                '👀 <b>Это возможно, но не гарантировано.</b>',
                '🔮 <b>Похоже на правду.</b>',
                '🔍 <b>Сомневаюсь, но всегда есть шанс.</b>',
                '⚖️ <b>Да, но с нюансами.</b>',
                '❓ <b>Ответ скорее да, чем нет.</b>',
                '👀 <b>Смотря как посмотреть, но скорее да.</b>',
                '🔮 <b>Не думаю, что это возможно.</b>',
                '🔍 <b>Не стоит на это надеяться.</b>',
                '⚖️ <b>Я не могу сказать точно.</b>',
                '❓ <b>Сложный вопрос.</b>',
                '👀 <b>Не вижу причин для сомнений.</b>',
                '🔮 <b>Спорно, но возможно.</b>',
                '🔍 <b>Ну, скорее нет, чем да.</b>',
                '⚖️ <b>Подождите немного, я думаю...</b>',
                '❓ <b>По всей видимости, да.</b>',
                '👀 <b>Это не исключено.</b>',
                '🔮 <b>Возможно, но не факт.</b>',
                '🔍 <b>Я бы сказал - да, но...</b>',
                '⚖️ <b>Лучше не рассчитывать на это.</b>',
                '❓ <b>Наверное, нет.</b>',
                '👀 <b>Похоже, что да.</b>',
                f"🔮 <b>Спроси у <a href='tg://user?id={user_id}'>{name}</a>.</b>",
                f"🔍 <b>Я уверен, что <a href='tg://user?id={user_id}'>{name}</a> знает ответ.</b>"
            ]
            await message.answer(
                f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> {random.choice(danet)}",
                parse_mode="HTML")


@rate_limit(limit=2)
async def who(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        words_after_bot_kto = message.text[7:]
        user_id, name = db_group.random_user_with_name_from_user_messages_table()
        who = [
            f"Я думаю что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}"
            f"Легенда гласит, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Мой кот думает, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"По всей видимости <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Безусловно <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Слухи утверждают, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Согласно моим данным <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Загадочный мир ботов утверждает, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Мои боты-коллеги утверждают, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Моя интуиция подсказывает, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Ясно вижу, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
            f"Ну тут даже мне понятно, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}"
        ]
        await message.answer(
            f"{random.choice(who)}",
            parse_mode="HTML")


@rate_limit(limit=2)
async def infa(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        await message.answer(
            f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"
            f" Судя по данным, вероятность составляет {random.randint(0, 100)}%.",
            parse_mode="HTML")


async def user_all(message: types.Message):
    mat = [
        'суко',
        'твор',
        'твар',
        'бляд',
        'какашка',
        'пиздец',
        'писдец',
        'блят',
        'билят',
        'биля',
        'бля',
        'ебал',
        'ебу',
        'ебанат',
        'еблан',
        'чурка',
        'сперма',
        'трохоты',
        'трахать',
        'трахав',
        'трахнув',
        'сосав',
        'сосать',
        'писюн',
        'хуй',
        'писька',
        'пэсюн',
        'лоха',
        'лох',
        'ахуенный,',
        'ахуеть',
        'ахуел',
        'похуй',
        'мать',
        'динаху',
        'ди наху',
        'гандон',
        'нихуя',
        'схуяли',
        'блять',
        'блят',
        'Апездал',
        'Апездошенна',
        'Блядь',
        'Блядство',
        'Выебон',
        'Выебать',
        'Вхуюжить',
        'Гомосек',
        'Долбоёб',
        'Ебло',
        'Еблище',
        'Ебать',
        'Ебическая сила',
        'Ебунок',
        'Еблан',
        'Ёбнуть',
        'Ёболызнуть',
        'Ебош',
        'Заебал',
        'Заебатый',
        'Злаебучий',
        'Заёб',
        'Иди на хуй',
        'Колдоебина',
        'Манда',
        'Мандовошка',
        'Мокрощелка',
        'Наебка',
        'Наебал',
        'Наебаловка',
        'Напиздеть',
        'Отъебись',
        'Охуеть',
        'Отхуевертить',
        'Опизденеть',
        'Охуевший',
        'Отебукать',
        'Пизда',
        'Пидарас',
        'Пиздатый',
        'Пиздец',
        'Пизданутый',
        'Поебать',
        'Поебустика',
        'Проебать',
        'Подзалупный',
        'Пизденыш',
        'Припиздак',
        'Разъебать',
        'Распиздяй',
        'Разъебанный',
        'Сука',
        'Сучка',
        'Трахать',
        'Уебок',
        'Уебать',
        'Угондошить',
        'Уебан',
        'Хитровыебанный',
        'Хуй',
        'Хуйня',
        'Хуета',
        'Хуево',
        'Хуесос',
        'Хуеть',
        'Хуевертить',
        'Хуеглот',
        'Хуистика',
        'Членосос',
        'Членоплет',
        'Шлюха'
    ]
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


def register_client(dp: Dispatcher):
    dp.register_message_handler(config, is_admin=True, commands=['config'])
    dp.register_message_handler(danet, regexp=re.compile(r'^\.данет'))
    dp.register_message_handler(who, lambda message: message.text.lower().startswith("бот кто"))
    dp.register_message_handler(infa, lambda message: message.text.lower().startswith("бот инфа"))
    dp.register_message_handler(say, lambda message: message.text.lower().startswith("добряк скажи"))
    dp.register_message_handler(here, lambda message: message.text.lower().startswith(("мовп ты тута", "мовп ты тут")))
    # dp.register_message_handler(profile, text=['.профиль'])
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(rules, commands=['rules'])
    dp.register_message_handler(delete, text=['.удалить правила'])
    dp.register_message_handler(dobryak, text=['добряк', 'Добряк', 'Доприяк', 'доприк', "Бойбака", "бойбака"])
    dp.register_message_handler(bot, text=['бот', 'Бот', 'Ботык', 'ботик', "ботык", "Ботик"])
    dp.register_message_handler(comand_list, commands=['commands'])
    dp.register_message_handler(song, text=['эй браточик песенку сыграй ка'])
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
    dp.register_message_handler(user_all)
