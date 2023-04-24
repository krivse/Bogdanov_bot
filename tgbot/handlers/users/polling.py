from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType

from tgbot.keyboards.inline import cancel_poll, options_poll
from tgbot.misc.states import PollState
from tgbot.services.set_commands import commands


async def polling_handler(message: Message):
    """Создание голосования в группе."""
    await message.answer(
        'Напишите вопрос для голосования',
        reply_markup=cancel_poll
    )
    await PollState.question.set()


async def polling_handler_inline(call: CallbackQuery):
    """Создание голосования в группе inline-режиим."""
    await call.message.answer(
        'Напишите вопрос для голосования',
        reply_markup=cancel_poll
    )
    await PollState.question.set()


async def question_setting(message: Message, state: FSMContext):
    """Настройка вопроса для голосования"""
    question = message.text
    if question not in commands:
        await message.answer(
            'Напишите ответ и отправьте. После ввода всех ответов нажмите на кнопку "Далее".'
            'Количество ответов может быть от 2 до 10 включительно, каждый из 1-100 символов',
            reply_markup=options_poll)
        await state.update_data(question=question)
        await PollState.options.set()
    else:
        await message.answer('Вопрос должен состояить из 1-255 символов.'
                             'Не может быть иметь название комманды бота.')


async def options_setting(message: Message, list_options: list):
    """Настройка ответов для голосования."""
    option = message.text.capitalize()
    if 10 >= len(list_options) and option not in list_options:
        # добавление варианта ответа  в список
        list_options.append(option)
        await message.answer(f'Вы добавили новый вариант ответа {option}. Количество ответов {len(list_options)}')
    elif option in list_options:
        await message.answer(f'Вы уже добавили такой вариант ответа: {option}. Попробуйте снова..')
    elif len(list_options) == 10:
        await message.answer('Вы добавили максильмальное кол-во ответов 10, нажмите на кнопку "Далее"!')


async def options_next(call: CallbackQuery, state: FSMContext, list_options):
    """Потверждение ввода вариантов ответов или сброс состояния пользователя."""
    if len(list_options) < 2:
        await call.message.answer(
            f'Попробуйте снова... Напишите ещё варианты ответов. Вы ввели {len(list_options)} ответа. '
            'Количество ответов должно быть от 2 до 10 включительно, каждый из 1-100 символов.',
            reply_markup=cancel_poll
        )
        await PollState.options.set()
    else:
        # добавление списка ответов в машину-состояния
        await call.message.answer('Ваш опрос создан и отправлен в группу.')

        # cоздание голосования и отправка в группу
        data = await state.get_data()
        question = data.get('question')
        group_chat = call.message.bot.get('config').tg_bot.group_ids[0]

        await call.message.bot.send_poll(
            chat_id=group_chat,
            question=question,
            options=list_options
        )
        # сброс списка ответов
        list_options.clear()
        # сброс состояния пользователя
        await state.finish()


async def poll_cancel(call: CallbackQuery, state: FSMContext, list_options: list):
    """Сброс мащина-состояния и списка ответов."""
    await call.message.answer('Можете начать сначала /create_poll')
    await state.finish()
    await call.message.edit_reply_markup()
    list_options.clear()


def register_user_polling(dp: Dispatcher):
    dp.register_message_handler(polling_handler, Command('create_poll'), content_types=ContentType.TEXT)
    dp.register_callback_query_handler(polling_handler_inline, text='create_poll')
    dp.register_message_handler(question_setting, state=PollState.question, content_types=ContentType.TEXT)
    dp.register_message_handler(options_setting, state=PollState.options, content_types=ContentType.TEXT)
    dp.register_callback_query_handler(options_next, text='next_step', state=PollState.states)
    dp.register_callback_query_handler(poll_cancel, text='cancel_poll', state=PollState.states)