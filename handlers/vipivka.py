import random

from aiogram import types, Dispatcher
from database.db import Database_group_beer, Database_group_vodka, Database_group_iq
from antiflood import rate_limit

db_drink = Database_group_beer('bd.db')
db_vodka = Database_group_vodka('bd.db')
db_iq = Database_group_iq('bd.db')


@rate_limit(limit=2)
async def beer(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_id = message.from_user.id
            group_id = message.chat.id
            full_name = message.from_user.full_name
            liters = random.uniform(1, 15)

            if db_drink.check_message_time(user_id, group_id):
                db_drink.add_message(user_id, group_id, full_name, liters)
                await message.answer(
                    f"<a href='tg://user?id={user_id}'>{message.from_user.full_name}</a> выпил целых {round(liters, 2)} литров пива\n"
                    f"Всего выпито {round(db_drink.get_liters(message.from_user.id, message.chat.id), 2)} литров",
                    parse_mode="HTML")
            else:
                await message.answer(
                    f"Следующий попытка выпить пивка будет доступна через {db_drink.remaining_time(message.from_user.id, message.chat.id)}")


@rate_limit(limit=2)
async def beer_all_the_group(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_data = db_drink.get_users_and_liters_in_group(message.chat.id)
            sorted_data = sorted(user_data, key=lambda x: x[1], reverse=True)
            text = "\n".join([f'{name} - {round(litr, 2)} литров' for name, litr in sorted_data])
            await message.answer(text)


@rate_limit(limit=2)
async def beer_all(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_data = db_drink.get_all_users_and_liters()
            sorted_data = sorted(user_data, key=lambda x: x[1:], reverse=True)
            text = '\n'.join([f"{name} - {round(litr, 2)} литров" for name, litr in sorted_data])
            await message.answer(text)


""""""""""""""""""""""""""""""""""""""""""""""""""""""


@rate_limit(limit=2)
async def vodka(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_id = message.from_user.id
            group_id = message.chat.id
            full_name = message.from_user.full_name
            liters = random.uniform(1, 15)

            if db_vodka.check_message_time(user_id, group_id):
                db_vodka.add_message(user_id, group_id, full_name, liters)
                await message.answer(
                    f"<a href='tg://user?id={user_id}'>{message.from_user.full_name}</a> выпил целых {round(liters, 2)} литров водки\n"
                    f"Всего выпито {round(db_vodka.get_liters(message.from_user.id, message.chat.id), 2)} литров",
                    parse_mode="HTML")
            else:
                await message.answer(
                    f"Следующий попытка выпить водяры будет доступна через {db_vodka.remaining_time(message.from_user.id, message.chat.id)}")


@rate_limit(limit=2)
async def vodka_all_the_group(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_data = db_vodka.get_users_and_liters_in_group(message.chat.id)
            sorted_data = sorted(user_data, key=lambda x: x[1], reverse=True)
            text = "\n".join([f'{name} - {round(litr, 2)} литров' for name, litr in sorted_data])
            await message.answer(text)


@rate_limit(limit=2)
async def vodka_all(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_data = db_vodka.get_all_users_and_liters()
            sorted_data = sorted(user_data, key=lambda x: x[1:], reverse=True)
            text = '\n'.join([f"{name} - {round(litr, 2)} литров" for name, litr in sorted_data])
            await message.answer(text)


""""""""""""""""""""""""""""""""""""""""""""""""""""""


@rate_limit(limit=2)
async def iq(message: types.Message):
    if message.from_user.id == 1122450298:
        await message.reply('пшов нахуй зсвидсы')
    else:
        if message.chat.type != types.ChatType.PRIVATE:
            user_id = message.from_user.id
            group_id = message.chat.id
            full_name = message.from_user.full_name
            liters = random.uniform(-20, 15)

            if db_iq.check_message_time(user_id, group_id):
                db_iq.add_message(user_id, group_id, full_name, liters)
                if liters < 0:
                    await message.answer(
                        f"<a href='tg://user?id={user_id}'>{message.from_user.full_name}</a>, за последнее время, "
                        f"ваш IQ снизилися на {str(round(liters, 2))[1:]}\n\n"
                        f"Тепер ваш IQ составляет {round(db_iq.get_liters(message.from_user.id, message.chat.id), 2)}",
                        parse_mode="HTML")
                else:
                    await message.answer(
                        f"<a href='tg://user?id={user_id}'>{message.from_user.full_name}</a> поздравляем, "
                        f"ваш IQ повысился на {round(liters, 2)}\n\n"
                        f"Тепер ваш IQ составляет {round(db_iq.get_liters(message.from_user.id, message.chat.id), 2)}",
                        parse_mode="HTML")
            else:
                await message.answer(
                    f"Следующай попытка будет доступна через {db_iq.remaining_time(message.from_user.id, message.chat.id)}")


@rate_limit(limit=2)
async def iq_all_the_group(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_data = db_iq.get_users_and_liters_in_group(message.chat.id)
            sorted_data = sorted(user_data, key=lambda x: x[1], reverse=True)
            text = "\n".join([f'{name} {round(litr, 2)} iq' for name, litr in sorted_data])
            await message.answer(text)


@rate_limit(limit=2)
async def iq_all(message: types.Message):
    if message.from_user.id != 1122450298:
        if message.chat.type != types.ChatType.PRIVATE:
            user_data = db_iq.get_all_users_and_liters()
            sorted_data = sorted(user_data, key=lambda x: x[1:], reverse=True)
            text = '\n'.join([f"{name} {round(litr, 2)} iq" for name, litr in sorted_data])
            await message.answer(text)


def register_drink(dp: Dispatcher):
    dp.register_message_handler(beer, commands=['beer'])
    dp.register_message_handler(beer_all_the_group, commands=['top_beer'])
    dp.register_message_handler(beer_all, commands=['all_beer'])
    dp.register_message_handler(vodka, commands=['vodka'])
    dp.register_message_handler(vodka_all_the_group, commands=['top_vodka'])
    dp.register_message_handler(vodka_all, commands=['all_vodka'])
    dp.register_message_handler(iq, commands=['iq'])
    dp.register_message_handler(iq_all, commands=['top_iq'])
    dp.register_message_handler(iq_all_the_group, commands=['all_iq'])
