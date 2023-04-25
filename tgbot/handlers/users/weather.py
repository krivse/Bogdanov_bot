from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType

from tgbot.keyboards.inline import cancel_weather
from tgbot.misc.states import WeatherState
from tgbot.services.owns import get_weather
from tgbot.services.set_commands import commands


async def weather_handler(message: Message, state: FSMContext):
    """Вывод сообщения о погоде в городе."""
    msg_for_delete_weather = await message.answer(
        'Чтобы узнать погоду введите название города',
        reply_markup=cancel_weather
    )
    await WeatherState.weather.set()

    # передаем в машину-состоние сообщение для удаления
    await state.update_data(msg_for_delete_weather=msg_for_delete_weather.message_id)


async def weather_handler_inline(call: CallbackQuery, state: FSMContext):
    """Вывод сообщения о погоде в городе c помощью inline-меню."""
    msg_for_delete_weather = await call.message.answer(
        'Чтобы узнать погоду введите название города',
        reply_markup=cancel_weather
    )
    await WeatherState.weather.set()

    # передаем в машину-состоние сообщение для удаления
    await state.update_data(msg_for_delete_weather=msg_for_delete_weather.message_id)


async def get_weather_handler(message: Message, own, state: FSMContext):
    """Вывод сообщения о погоде в городе."""
    msg_city = message.text

    if isinstance(msg_city, str) and msg_city not in commands:
        w = await get_weather(msg_city, own)
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


async def cancel_get_weather(call: CallbackQuery, state: FSMContext):
    """Сброс машина-состояния / удаление информационного сообщения."""
    msg_for_delete_weather = (await state.get_data()).get('msg_for_delete_weather')
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=msg_for_delete_weather)
    await state.finish()


def register_user_weather(dp: Dispatcher):
    dp.register_message_handler(weather_handler, Command('weather'), content_types=ContentType.TEXT)
    dp.register_callback_query_handler(weather_handler_inline, text='get_weather')
    dp.register_message_handler(get_weather_handler, state=WeatherState.weather, content_types=ContentType.TEXT)
    dp.register_callback_query_handler(cancel_get_weather, state=WeatherState.states, text='cancel_weather')
