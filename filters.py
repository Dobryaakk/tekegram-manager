from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class IsAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool, error_message: str = "У вас нет прав администратора!"):
        self.is_admin = is_admin
        self.error_message = error_message

    async def check(self, event):
        if isinstance(event, types.Message):
            chat_id = event.chat.id
            user_id = event.from_user.id
        elif isinstance(event, types.CallbackQuery):
            chat_id = event.message.chat.id
            user_id = event.from_user.id
        else:
            return False

        member = await event.bot.get_chat_member(chat_id, user_id)
        if member.is_chat_admin() == self.is_admin:
            return True
        else:
            if isinstance(event, types.Message):
                await event.reply(self.error_message)
            elif isinstance(event, types.CallbackQuery):
                await event.answer(self.error_message, show_alert=True)
            return False