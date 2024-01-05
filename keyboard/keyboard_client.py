from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""""""""""""""""""""""""""""""""""""старт"""""""""""""""""""""""""""""""""""""


def button_add_start() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить в чат', url='https://t.me/dcksckdscksdck_bot?startgroup=new')]
    ])
    return markup


def list_back() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data='menu')],
    ])
    return markup


# def setting_one() -> InlineKeyboardMarkup:
#     markup_setting_one = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton("Настройки бота", callback_data='sett'),
#          InlineKeyboardButton(text="Language", callback_data="start_language")]
#     ])
#     return markup_setting_one


########################################################################################################################

# def language() -> InlineKeyboardMarkup:
#     markup_lang = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text='English', callback_data='start_eng'),
#          InlineKeyboardButton(text="Русский", callback_data="start_ru")],
#         [InlineKeyboardButton(text="Українська", callback_data='start_ua'),
#          InlineKeyboardButton(text="Español", callback_data="start_spain")],
#         [InlineKeyboardButton(text="Отмена", callback_data='start_close')]
#     ])
#     return markup_lang


"""""""""""""""""""""""""""""""""""""настройки"""""""""""""""""""""""""""""""""""""


def setting_menu() -> InlineKeyboardMarkup:
    setting_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Список команд', callback_data='menu_list')],
        [InlineKeyboardButton(text="Правила", callback_data="menu_rules"),
         InlineKeyboardButton(text="Приветсвие", callback_data="well_welcome")],
        [InlineKeyboardButton(text="Предупреждения", callback_data='menu_pred')],
        [InlineKeyboardButton(text='Закрыть', callback_data='menu_close')]
    ])
    return setting_menu


def back() -> InlineKeyboardMarkup:
    back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В главное меню", callback_data="menu")],
        [InlineKeyboardButton(text='Поменять правила', callback_data='menu_rules')]
    ])
    return back


########################################################################################################################

def rules() -> InlineKeyboardMarkup:
    rules = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавть текст", callback_data="menu_add_rules"),
         InlineKeyboardButton(text='Просмотр', callback_data='menu_rules_see')],
        [InlineKeyboardButton(text='Отмена', callback_data='menu')]
    ])
    return rules


def rules_back() -> InlineKeyboardMarkup:
    rules_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="menu_add_rules_back")]
    ])
    return rules_back


def rules_back_fsm() -> InlineKeyboardMarkup:
    rules_back_fsm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="menu_fsm_rules_back")]
    ])
    return rules_back_fsm


########################################################################################################################

def back_welcome() -> InlineKeyboardMarkup:
    back_welcome = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В главное меню", callback_data="well")],
        [InlineKeyboardButton(text='Поменять приветствие', callback_data='well_welcome')]
    ])
    return back_welcome


def welcome() -> InlineKeyboardMarkup:
    welcome = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавть текст", callback_data="well_add_welcome"),
         InlineKeyboardButton(text='Просмотр', callback_data='well_welcome_see')],
        [InlineKeyboardButton(text='Назад', callback_data='well')]
    ])
    return welcome


def welcom_close() -> InlineKeyboardMarkup:
    welcome_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="well_add_welcome_back")]
    ])
    return welcome_back


def welcome_back_fsm() -> InlineKeyboardMarkup:
    welcome_back_fsm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="well_fsm_welcome_back")]
    ])
    return welcome_back_fsm


########################################################################################################################
def pred() -> InlineKeyboardMarkup:
    spam = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Настроить", callback_data='pred_on')],
        [InlineKeyboardButton(text="Назад", callback_data="well")]
    ])
    return spam


def pred_back_fsm() -> InlineKeyboardMarkup:
    spam = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="pred_fsm_back")]
    ])
    return spam


def pred_back() -> InlineKeyboardMarkup:
    spam = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="pred_back_count")]
    ])
    return spam


def create_pred_sett_keyboard(pred_value, pred_dead):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список предупреждений", callback_data="pred_list")],
        [InlineKeyboardButton(text="Кик" + (' ✅' if pred_dead == 'kick' else ''), callback_data="pred_kick")],
        [InlineKeyboardButton(text='Бан' + (' ✅' if pred_dead == 'bun' else ''), callback_data='pred_bun')],
        [InlineKeyboardButton(text='1' + (' ✅' if pred_value == 1 else ''), callback_data='pred_one'),
         InlineKeyboardButton(text='2' + (' ✅' if pred_value == 2 else ''), callback_data='pred_two'),
         InlineKeyboardButton(text='3' + (' ✅' if pred_value == 3 else ''), callback_data='pred_three'),
         InlineKeyboardButton(text='4' + (' ✅' if pred_value == 4 else ''), callback_data='pred_four'),
         InlineKeyboardButton(text="5" + (' ✅' if pred_value == 5 else ''), callback_data='pred_five')],
        [InlineKeyboardButton(text="Назад", callback_data="pred_back")]
    ])
    return keyboard
