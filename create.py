from aiogram import Bot, Dispatcher
from config.config import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from antiflood import ThrottlingMiddleware

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
throttling_middleware = ThrottlingMiddleware(limit=3)
dp.middleware.setup(throttling_middleware)