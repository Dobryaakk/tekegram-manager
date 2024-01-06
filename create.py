from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from antiflood import ThrottlingMiddleware

from database.config_db import host, user, password, db_name
from config.config import *
from database.fun_db import Database_group_iq, Database_group_beer, Database_group_vodka
from database.mute import Database_mute
from database.counter_word import Database_group_words, Database_group_bad_words, Database_group_words_day, Database_group_bad_words_day
from database.rules_welcome import Database_welcome, Database_rules
from database.pred import Database_pred, Database_pred_dead, Database_pred_user
from database.users import Database_group, Database_user_all


fun_db_beer = Database_group_beer(host, user, password, db_name)
fun_db_vodka = Database_group_vodka(host, user, password, db_name)
fun_db_iq = Database_group_iq(host, user, password, db_name)

mute_db = Database_mute(host, user, password, db_name)

db_words = Database_group_words(host, user, password, db_name)
db_add_bad = Database_group_bad_words(host, user, password, db_name)
db_add_day = Database_group_words_day(host, user, password, db_name)
db_bad_day = Database_group_bad_words_day(host, user, password, db_name)

welcome_db = Database_welcome(host, user, password, db_name)
db_rules = Database_rules(host, user, password, db_name)

db_pred_user = Database_pred_user(host, user, password, db_name)
db_pred = Database_pred(host, user, password, db_name)
db_pred_dead = Database_pred_dead(host, user, password, db_name)

db_group = Database_group(host, user, password, db_name)
db_add_user = Database_user_all(host, user, password, db_name)


storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
throttling_middleware = ThrottlingMiddleware(limit=3)
dp.middleware.setup(throttling_middleware)