from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

actions_after_creating_stickerset_buttons = [
    [InlineKeyboardButton(text='Готово', callback_data='done_button')]
]

actions_after_creating_stickerset_kb = InlineKeyboardMarkup(inline_keyboard=actions_after_creating_stickerset_buttons)