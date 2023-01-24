from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    help_button = KeyboardButton('/help')
    add_button = KeyboardButton('/add')
    stats_button = KeyboardButton('/stats')
    billings_button = KeyboardButton('/billings')
    return keyboard.add(help_button).insert(add_button) \
        .add(stats_button).insert(billings_button)


def cancel_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    ).add(KeyboardButton('/cancel'))
