from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.inline import menu


async def admin_start(message: Message):
    """Начало работы бота с администратором."""
    await message.reply(
        f'Приветствую в многофунциональном боте, {message.from_user.full_name} (admin)\n'
        f'Выберите интересующий пункт меню',
        reply_markup=menu)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
