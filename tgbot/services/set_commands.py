from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat
from aiogram.bot import Bot

commands = [
    '/start'
    '/weather',
    '/currency_conversion',
    '/create_poll'
    '/random_image'
]


async def set_default_commands(bot: Bot, user_id):
    """
    Команды для пользователя general_commands
    Команды для админа general_commands + дополнительные."""
    general_commands = [
        BotCommand('start', 'Начало работы'),
        BotCommand('weather', 'Погода'),
        BotCommand('currency_conversion', 'Конвертация валют'),
        BotCommand('poll', 'Создание опросов'),
        BotCommand('random_image', 'Милое животное')
    ]
    if user_id in bot.get('config').tg_bot.admin_ids:
        await bot.set_my_commands(
            commands=[
                *general_commands,
                # команды для админа
            ],
            scope=BotCommandScopeChat(user_id)
        )
    else:
        await bot.set_my_commands(
            commands=general_commands,
            scope=BotCommandScopeAllPrivateChats()
        )
