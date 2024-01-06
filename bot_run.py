from aiogram import executor

from create import dp
from filters import IsAdminFilter
from handlers import client, settings, vipivka, pred, chat_off_on, chat_member, ban_kick
from handlers import mute


def start():
    vipivka.register_drink(dp)
    pred.register_pred(dp)
    ban_kick.register_ban_kick(dp)
    chat_member.register_chat_member(dp)
    chat_off_on.register_chat_off_on(dp)
    mute.register_mute(dp)
    settings.register_callback(dp)

    client.register_top_commands(dp)
    client.register_commands(dp)
    client.register_user_all(dp)


if __name__ == "__main__":
    dp.filters_factory.bind(IsAdminFilter)
    start()
    executor.start_polling(dp, skip_updates=True)
