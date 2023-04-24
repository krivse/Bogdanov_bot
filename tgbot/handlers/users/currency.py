from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery, ContentType

from py_currency_converter.py_exchange_rate import country_codes

from tgbot.keyboards.inline import currency_base, list_currency_to
from tgbot.misc.states import CurrencyState
from tgbot.services.conversion import currency_conversion


async def currency_handler(message: Message, state: FSMContext):
    """Вывод сообщения с inline кнопками "валют" для конвертации."""
    msg_for_delete_currency = await message.answer(
        'Выберите базовую валюту для конвертациия',
        reply_markup=await currency_base()
    )

    # передаем в машину-состоние сообщение для удаления
    await state.update_data(msg_for_delete_currency=msg_for_delete_currency.message_id)


async def currency_handler_inline(call: CallbackQuery, state: FSMContext):
    """Вывод сообщения c выбором валют c помощью inline-меню."""
    msg_for_delete_currency = await call.message.answer(
        'Выберите базовую валюту для конвертациия',
        reply_markup=await currency_base()
    )
    await state.update_data(msg_for_delete_currency=msg_for_delete_currency.message_id)


async def choose_currency(call: CallbackQuery, state: FSMContext, list_currency):
    """Выбор одной или нескольких валют для конвертации."""
    base_currency = (await state.get_data()).get('base_currency')

    if base_currency is None:
        msg_for_delete_currency = (await state.get_data()).get('msg_for_delete_currency')

        await call.message.edit_reply_markup()
        await call.message.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_for_delete_currency)

        msg_for_delete_currency = await call.message.answer(
            f'Выберите одну или несколько валют в которую хотите конвертировать',
            reply_markup=await list_currency_to()
        )
        await state.update_data(
            base_currency=call.data,
            msg_for_delete_currency=msg_for_delete_currency.message_id
        )
    else:
        # выбор пар для конвертации относительно базовой валюты
        list_currency.append(call.data)


async def next_currency(call: CallbackQuery, state: FSMContext, list_currency):
    """Добавление в машину-состояние списка из валют для конвертации"""
    msg_for_delete_currency = (await state.get_data()).get('msg_for_delete_currency')
    await call.message.edit_reply_markup()
    await call.message.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_for_delete_currency)

    await state.update_data(list_currency_to=list_currency)
    await call.message.answer('Введите сумму для рассчёта конвертации')

    await CurrencyState.amount.set()


async def get_currency_conversion(message: Message, state: FSMContext, list_currency):
    """Конвертация выбранной валюты."""
    data = await state.get_data()
    # проверка, что сумма является числом
    if message.text.isdigit():
        base_currency = data.get('base_currency')
        currency_to = data.get('list_currency_to')
        amount = float(message.text)
        result = await currency_conversion(base_currency, amount, currency_to)
        await message.answer(result)

        # сброс состояния пользователя с данными
        await state.finish()

        # отчистка спика от добавленных значений
        list_currency.clear()
    else:
        await message.answer('Сумма может быть только числом! Попробуйте снова..')


async def cancel_menu_with_list_currency(call: CallbackQuery, state: FSMContext):
    """Удаление клавиатуры / информационного сообщения."""
    msg_for_delete_currency = (await state.get_data()).get('msg_for_delete_currency')
    await call.message.edit_reply_markup()
    await call.bot.delete_message(chat_id=call.from_user.id, message_id=msg_for_delete_currency)
    await state.reset_state(with_data=False)


def register_user_currency(dp: Dispatcher):
    dp.register_message_handler(currency_handler, Command('currency_conversion'))
    dp.register_callback_query_handler(currency_handler_inline, text='currency_conversion')
    dp.register_callback_query_handler(choose_currency, text=country_codes)
    dp.register_callback_query_handler(next_currency, text='next')
    dp.register_message_handler(get_currency_conversion, state=CurrencyState.amount, content_types=ContentType.TEXT)
    dp.register_callback_query_handler(cancel_menu_with_list_currency, text='cancel_currency')
