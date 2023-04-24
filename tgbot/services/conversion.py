from py_currency_converter import convert


def currency_conversion(base: str, amount: float, to: list) -> str:
    """

    :param base: базовая валюта
    :param amount: сумма конвертации
    :param to: список валюты для рассчета
    :return: информационное сообщение
    """
    result = convert(base=base, amount=amount, to=to)
    string = ", ".join([f"{key}: {value}" for key, value in result.items()])

    return f'Конвертация из {base}, сумма {amount} в: {string}'
