from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.keyboards.inline import menu
from tgbot.services.set_commands import set_default_commands


async def user_start(message: Message, state: FSMContext):
    """Привествие пользователя и вывод inline клавиатуры для выбора функций по работе с ботой."""
    msg_menu_for_delete = await message.answer(
        f'Приветствую в многофунциональном боте, {message.from_user.full_name}\n'
        f'Выберите интересующий пункт меню',
        reply_markup=menu)

    # подключение пользовательских команд
    await set_default_commands(
        message.bot,
        user_id=message.from_id)

    # передаем в машину-состоние сообщение для удаления
    await state.update_data(msg_menu_for_delete=msg_menu_for_delete.message_id)


async def cancel_menu(call: CallbackQuery, state: FSMContext):
    """Удаление клавиатуры menu / информационного сообщения."""
    msg_for_delete = (await state.get_data()).get('msg_menu_for_delete')
    await call.message.edit_reply_markup()
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=msg_for_delete)
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, CommandStart(), state="*", content_types=ContentType.TEXT)
    dp.register_callback_query_handler(cancel_menu, text='cancel')
