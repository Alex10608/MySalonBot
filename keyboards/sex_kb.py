from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.cancel_kb import cancel_button

male_button = InlineKeyboardButton(
        text='Мужской',
        callback_data='male'
)
female_button = InlineKeyboardButton(
        text='Женский',
        callback_data='female'
)
keyboard: list[list[InlineKeyboardButton]] = [
        [male_button, female_button],
        [cancel_button]
]
sex_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)