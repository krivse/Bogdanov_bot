from datetime import date

from py_currency_converter import convert


async def currency_conversion(base: str, amount: float, to: list) -> str:
    """
    Запрос в Exchange Rates API для конвертации валюты
    :param base: базовая валюта
    :param amount: сумма конвертации
    :param to: список валюты для рассчета
    :return: информационное сообщение
    """

    # запускает выполнение этой функции в отдельном потоке и продолжает выполнять асинхронный код в текущем потоке
    from bot import loop
    result = await loop.run_in_executor(None, convert, base, date.today(), amount, to)

    # обработка результата
    string = ", ".join([f"{key}: {value}" for key, value in result.items()])

    return f'Конвертация из {base}, сумма {round(amount, 2)} в: {string}'
