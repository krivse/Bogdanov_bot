import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.handlers.users.animals import register_user_image
from tgbot.handlers.users.currency import register_user_currency
from tgbot.handlers.users.polling import register_user_polling
from tgbot.services.owns import config_weather
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.users.user import register_user
from tgbot.handlers.users.weather import register_user_weather
from tgbot.handlers.errors import register_errors_handler
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, own):
    list_currency: list = []
    list_options: list = []
    dp.setup_middleware(EnvironmentMiddleware(
        config=config, own=own, list_currency=list_currency, list_options=list_options)
    )


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_user_polling(dp)
    register_user_weather(dp)
    register_user_currency(dp)
    register_user_image(dp)
    register_errors_handler(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    # экземпляр настроек для работы с API own (OpenWeatherMap)
    own = config_weather(token=config.misc.own_token)

    register_all_middlewares(dp, config, own)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
