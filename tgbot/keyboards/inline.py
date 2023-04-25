from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from py_currency_converter.py_exchange_rate import country_codes


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Погода', callback_data='get_weather'),
        ],
        [
            InlineKeyboardButton(text='Конвертация валют', callback_data='currency_conversion')
        ],
        [
            InlineKeyboardButton(text='Создание опросов', callback_data='create_poll')
        ],
        [
            InlineKeyboardButton(text='Милые животные', callback_data='honey_dogs')
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]
    ]
)

# список валют
list_codes = country_codes


async def currency_base() -> InlineKeyboardMarkup:
    """Генерация кнопок наименований валюты."""
    markup = InlineKeyboardMarkup(row_width=4)

    for name in list_codes:
        markup.insert(InlineKeyboardButton(
            text=name,
            callback_data=name))

    markup.add(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_currency'))

    return markup


async def list_currency_to() -> InlineKeyboardMarkup:
    """Генерация кнопок наименований валюты."""
    markup = InlineKeyboardMarkup(row_width=4)

    for name in list_codes:
        markup.insert(InlineKeyboardButton(
            text=name,
            callback_data=name))

    markup.add(
        InlineKeyboardButton(
            text='Далее',
            callback_data='next'),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_currency'))

    return markup


options_poll = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Далее', callback_data='next_step'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_poll')
        ]
    ]
)

cancel_poll = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_poll')
        ]
    ]
)

cancel_weather = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_weather')
        ]
    ]
)
