from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

stickerset_actions_list_buttons = [
    [InlineKeyboardButton(text='Добавить стикер', callback_data='add_sticker_to_stickerset')],
    [InlineKeyboardButton(text='Удалить стикерпак', callback_data='delete_stickerset')],
    [InlineKeyboardButton(text='Венуться в меню', callback_data='back_to_menu_button')]
]

stickerset_actions_list_kb = InlineKeyboardMarkup(inline_keyboard=stickerset_actions_list_buttons)