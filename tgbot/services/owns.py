import logging
from typing import Any, Union

from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
import datetime


def config_weather(token) -> OWM:
    """Сонфигурационный файл для PyOWM."""
    config = get_default_config()
    config['language'] = 'ru'

    owm = OWM(api_key=token, config=config)
    manage_weather = owm.weather_manager()

    return manage_weather


def get_weather(city, mgr) -> Union[dict[str, Union[str, Any]], bool]:
    """
    Получение погоды для разных городов по API (OpenWeatherMap).
    :param city: наименование города
    :param mgr: экземляр класса OWN с настройками для запросов
    :return: tuple[float, str, str, str]
    """
    w = {}
    try:
        weather = mgr.weather_at_place(city)
        w['temp'] = weather.weather.temperature('celsius')['temp']
        w['description'] = weather.weather.detailed_status
        w['location'] = weather.location.name
        w['time'] = datetime.datetime.fromtimestamp(weather.rec_time).strftime('%d-%m-%Y %H:%M:%S')
        return w
    except NotFoundError:
        return False
    except Exception as e:
        logging.error(f'Ошибка вызова PyOWM: {e}')
