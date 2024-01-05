from aiogram import types, Dispatcher
from database.db import Database_rules, Database_welcome, Database_language, Database_pred, \
    Database_pred_dead
from keyboard import keyboard_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.client import top_eblanov

db_rules = Database_rules('bd.db')
db_welcome = Database_welcome('bd.db')
db_lang = Database_language('bd.db')
db_pred = Database_pred('bd.db')
db_dead = Database_pred_dead('bd.db')
user_id_rul = None
user_id_priv = None


class FSM(StatesGroup):
    rules = State()
    welcome = State()
    pred = State()


# async def language(calback: types.CallbackQuery):
#     if calback.data == "start_language":
#         await calback.message.edit_text("Выберите язык", reply_markup=keyboard_client.language())
#     elif calback.data == 'start_close':
#         await calback.message.edit_text(
#             "Привет\n\nЯ чат менеджер, создан для управления чатами\n\nЧтобы добавить меня в чат нажми на кнопку ниже",
#             reply_markup=keyboard_client.button_add_start())
#     elif calback.data == 'start_ua':
#         db_lang.add_user_lang(calback.message.from_user.id, 'UA')


########################################################################################################################
async def setting_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("Настройки бота", reply_markup=keyboard_client.setting_menu())


########################################################################################################################
async def menu_setting(callback: types.CallbackQuery):
    if callback.data == 'menu_pred':
        await callback.message.edit_text('Нажав на кнопку "настроить" '
                                         'вы можете самостоятельно настроисть команду /pred',
                                         reply_markup=keyboard_client.pred())
    elif callback.data == 'menu_close':
        await callback.message.delete()
    elif callback.data == 'menu':
        await callback.message.edit_text("Настройки бота", reply_markup=keyboard_client.setting_menu())
    elif callback.data == 'menu_list':
        await callback.message.edit_text(
            "https://teletype.in/@dobrychek/q3QWyxkYax-",
            reply_markup=keyboard_client.list_back(), disable_web_page_preview=True)

    if callback.data == 'menu_rules':
        await callback.message.edit_text("Добавление правил", reply_markup=keyboard_client.rules())

    elif callback.data == 'menu_rules_see':
        await callback.message.edit_text(db_rules.get_rules(callback.message.chat.id),
                                         reply_markup=keyboard_client.rules_back())
        await callback.answer()

    elif callback.data == 'menu_add_rules_back':
        await callback.message.edit_text("Добавление правил", reply_markup=keyboard_client.rules())

    elif callback.data == 'menu_add_rules':
        global user_id_rul
        user_id_rul = callback.from_user.id
        await FSM.rules.set()
        await callback.message.edit_text("Введи текст", reply_markup=keyboard_client.rules_back_fsm())


async def rules(message: types.Message, state: FSMContext):
    global user_id_rul
    async with state.proxy() as data:
        data['rules'] = message.text

    if user_id_rul == message.from_user.id:
        db_rules.add_rules(message.chat.id, message.text)
        await message.answer('Правила успешно добавлены!\n'
                             'Удалить правила можна по команде <code>.удалить правила</code>',
                             reply_markup=keyboard_client.back(), parse_mode="HTML")
        await state.finish()
    else:
        await message.answer(
            '')


async def back_with_fsm_rules(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text("Добавление правил", reply_markup=keyboard_client.rules())


########################################################################################################################

async def welcome_setting(callback: types.CallbackQuery):
    if callback.data == 'well':
        await callback.message.edit_text("Добавление приветствия", reply_markup=keyboard_client.setting_menu())

    elif callback.data == 'well_welcome':
        await callback.message.edit_text("Добавление приветствия", reply_markup=keyboard_client.welcome())
    elif callback.data == 'well_welcome_see':
        await callback.message.edit_text(db_welcome.get_welcome(callback.message.chat.id),
                                         reply_markup=keyboard_client.welcom_close())
        await callback.answer()

    elif callback.data == 'well_add_welcome_back':
        await callback.message.edit_text("Добавление приветствия", reply_markup=keyboard_client.welcome())

    elif callback.data == 'well_add_welcome':
        global user_id_priv
        user_id_priv = callback.from_user.id
        await FSM.welcome.set()
        await callback.message.edit_text("Введи текст", reply_markup=keyboard_client.welcome_back_fsm())


async def welcome(message: types.Message, state: FSMContext):
    global user_id_priv
    async with state.proxy() as data:
        data['welcome'] = message.text

    if user_id_priv == message.from_user.id:
        db_welcome.add_welcome(message.chat.id, message.text)
        await message.answer('Приветствие успешно добавлено!', reply_markup=keyboard_client.back_welcome())
        await state.finish()
    else:
        await message.answer(
            'Ви намагаєтеся ввести приветствие від іншого користувача. Введіть /start, щоб розпочати процес знову.')


async def back_with_fsm_welcome(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text("Добавление приветствия", reply_markup=keyboard_client.welcome())


#######################################################################################################################
async def pred_settings(callback: types.CallbackQuery):
    if callback.data == 'pred_on' or callback.data == 'pred_litle':
        await callback.message.edit_text(
            'В данном меню настройте предупреждения так как хотите этого вы.\n\n'
            f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
            reply_markup=keyboard_client.create_pred_sett_keyboard(db_pred.get_default_pred_value(),
                                                                   db_dead.get_default_dead_text()))
    elif callback.data == "pred_back":
        await callback.message.edit_text(
            'Предупреждения выключены, что бы включить и настроить предупреждение нажмите на кнопку ниже',
            reply_markup=keyboard_client.pred())
    elif callback.data == 'pred_back_count':
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_one':
        db_pred.insert_or_update_data(callback.message.chat.id, 1)
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_two':
        db_pred.insert_or_update_data(callback.message.chat.id, 2)
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_three':
        db_pred.insert_or_update_data(callback.message.chat.id, 3)
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_four':
        db_pred.insert_or_update_data(callback.message.chat.id, 4)
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_five':
        db_pred.insert_or_update_data(callback.message.chat.id, 5)
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_bun':
        db_dead.insert_or_update_data_dead(callback.message.chat.id, 'bun')
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))

    elif callback.data == 'pred_kick':
        db_dead.insert_or_update_data_dead(callback.message.chat.id, 'kick')
        await callback.message.edit_text('В данном меню настройте предупреждения так как хотите этого вы.\n\n'
                                         f'Наказание: {db_dead.get_default_dead_text()}\nПредупреждений: {db_pred.get_default_pred_value()}',
                                         reply_markup=keyboard_client.create_pred_sett_keyboard(
                                             db_pred.get_default_pred_value(), db_dead.get_default_dead_text()))
    elif callback.data == 'pred_list':
        group_message = await top_eblanov(callback.message)
        await callback.message.edit_text(f'Пользователи и их количество предупреждений\n{group_message}',
                                         parse_mode='HTML', reply_markup=keyboard_client.pred_back())


def register_callback(dp: Dispatcher):
    # dp.register_callback_query_handler(language, lambda calback_query: calback_query.data.startswith('start'))

    dp.register_callback_query_handler(setting_callback, text='sett', is_admin=True)

    dp.register_callback_query_handler(menu_setting,
                                       lambda callback_query: callback_query.data.startswith('menu'), state=None,
                                       is_admin=True)
    dp.register_message_handler(rules, state=FSM.rules, is_admin=True)
    dp.register_callback_query_handler(back_with_fsm_rules, state="*", text='menu_fsm_rules_back', is_admin=True)

    dp.register_callback_query_handler(welcome_setting, lambda callback_query: callback_query.data.startswith('well'),
                                       state=None, is_admin=True)
    dp.register_message_handler(welcome, state=FSM.welcome, is_admin=True)
    dp.register_callback_query_handler(back_with_fsm_welcome, state="*", text='well_fsm_welcome_back', is_admin=True)

    dp.register_callback_query_handler(pred_settings, lambda callback_query: callback_query.data.startswith('pred'),
                                       is_admin=True)
