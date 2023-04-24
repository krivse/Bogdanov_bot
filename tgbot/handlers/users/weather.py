from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType

from tgbot.misc.states import WeatherState
from tgbot.services.owns import get_weather
from tgbot.services.set_commands import commands


async def weather_handler(message: Message):
    """Вывод сообщения о погоде в городе."""
    await message.answer('Чтобы узнать погоду введите название города')
    await WeatherState.weather.set()


async def weather_handler_inline(call: CallbackQuery):
    """Вывод сообщения о погоде в городе c помощью inline-меню."""
    await call.message.answer('Чтобы узнать погоду введите название города')
    await WeatherState.weather.set()


async def get_weather_handler(message: Message, own, state: FSMContext):
    """Вывод сообщения о погоде в городе."""
    msg_city = message.text

    if isinstance(msg_city, str) and msg_city not in commands:
        w = get_weather(msg_city, own)
        if isinstance(w, dict):
            await message.answer(
                f'Сегодня: {w.get("time")}\n'
                f'Погода в городе {w.get("location")} {int(w.get("temp"))}°C, {w.get("description")}')
            # Сбросить состояние пользователя
            await state.finish()
        elif not w:
            await message.answer('Вы ввели некрретное название города, попробую снова..')
    else:
        await message.answer('Укажите город, например: Москва')


def register_user_weather(dp: Dispatcher):
    dp.register_message_handler(weather_handler, Command('weather'), content_types=ContentType.TEXT)
    dp.register_callback_query_handler(weather_handler_inline, text='get_weather')
    dp.register_message_handler(get_weather_handler, state=WeatherState.weather, content_types=ContentType.TEXT)
