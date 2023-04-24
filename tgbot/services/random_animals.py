import asyncio
import logging

from aiogram.utils import exceptions

import aiohttp


async def get_random_image_url(dog_api_url):
    """Создание менедждера контекста асинхронного вызова."""
    async with aiohttp.ClientSession() as session:
        async with session.get(dog_api_url) as resp:
            url = (await resp.json())['url']
            return url


async def send_random_image():
    """Получение случайной картинки."""
    dog_api_url = 'https://random.dog/woof.json'
    image_url = await get_random_image_url(dog_api_url)

    ext = image_url.split('.')[-1]
    if ext.lower() in ('jpg', 'jpeg', 'png', 'bmp', 'gif'):
        try:
            return image_url, ext
        except exceptions.BadRequest as e:
            logging.error(f'Ошибка запрос: {e}')
