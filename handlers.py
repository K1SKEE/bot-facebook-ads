from aiogram import types
from aiogram.dispatcher import FSMContext

from utils import *
from buttons import menu_keyboard, cancel_keyboard
from services import *


async def bot_greetings(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user = get_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"{user} Вас вітає бот для Ads менеджера Facebook\n"
        f"Додавайте аккаунт FB та відслідковуйте всю "
        f"статистику з Ads\n"
        f"/help\n/add\n/stats\n/billing\n/billings\n/autoupdate",
        reply_markup=menu_keyboard())


async def cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await message.reply('Відмінено',
                        reply_markup=menu_keyboard())


async def add_handler(message: types.Message):
    await FBCredentialsStatesGroup.login.set()
    await message.answer('Введіть логін',
                         reply_markup=cancel_keyboard())


async def check_credentials(message: types.Message):
    return await message.reply('Неправильні данні')


async def set_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await FBCredentialsStatesGroup.next()
    await message.answer('Введіть пароль',
                         reply_markup=cancel_keyboard())


async def set_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await FBCredentialsStatesGroup.next()
    await message.answer('Введіть проксі',
                         reply_markup=cancel_keyboard())


async def set_proxy(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['proxy'] = message.text

        await message.answer('Авторизовуюсь')
        is_authorized = add_account(data.as_dict())
        if not is_authorized:
            await message.answer('Безуспішно')
        else:
            await message.answer('Успішно')
    await state.finish()


async def stats(message: types.Message):
    pass


def register_handlers(dispatcher):
    dispatcher.register_message_handler(bot_greetings,
                                        commands=['start', 'help'])
    dispatcher.register_message_handler(cancel,
                                        commands=['cancel', 'N'], state='*')
    dispatcher.register_message_handler(add_handler, commands=['add'],
                                        state=None)
    dispatcher.register_message_handler(check_credentials,
                                        lambda message: not message.text,
                                        state=FBCredentialsStatesGroup.states)
    dispatcher.register_message_handler(set_login,
                                        state=FBCredentialsStatesGroup.login)
    dispatcher.register_message_handler(set_password,
                                        state=FBCredentialsStatesGroup.password)
    dispatcher.register_message_handler(set_proxy,
                                        state=FBCredentialsStatesGroup.proxy)
