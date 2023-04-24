from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.services.random_animals import send_random_image


async def random_image_handler(message: Message):
    """Отправка пользователю случайной картинки."""
    image_url, ext = await send_random_image()
    # отправка изображения
    if image_url and ext != 'gif':
        await message.bot.send_photo(chat_id=message.chat.id, photo=image_url)
    # отправка гифки
    elif image_url and ext == 'gif':
        await message.bot.send_animation(chat_id=message.chat.id, animation=image_url)
    else:
        await message.answer('Ошибка запроса. Попробуйте позже..')


async def random_image_handler_inline(call: CallbackQuery):
    """Отправка пользователю случайной картинки inline-режим."""
    image_url, ext = await send_random_image()
    # отправка изображения
    if image_url and ext != 'gif':
        await call.message.bot.send_photo(chat_id=call.message.chat.id, photo=image_url)
    # отправка гифки
    elif image_url and ext == 'gif':
        await call.message.bot.send_animation(chat_id=call.message.chat.id, animation=image_url)
    else:
        await call.message.answer('Ошибка запроса. Попробуйте позже..')


def register_user_image(dp: Dispatcher):
    dp.register_message_handler(random_image_handler, Command('random_aimage'), content_types=ContentType.TEXT)
    dp.register_callback_query_handler(random_image_handler_inline, text='honey_animals')
