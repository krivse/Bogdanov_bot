from aiogram.dispatcher.filters.state import StatesGroup, State


class WeatherState(StatesGroup):
    weather = State()


class CurrencyState(StatesGroup):
    amount = State()


class PollState(StatesGroup):
    question = State()
    options = State()
    create = State()
