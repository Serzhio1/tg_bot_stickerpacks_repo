from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_delete_stickerset_buttons = [
    [InlineKeyboardButton(text='Да', callback_data='delete_stickerset_button')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')]
]

confirm_delete_stickerset_kb = InlineKeyboardMarkup(inline_keyboard=confirm_delete_stickerset_buttons)