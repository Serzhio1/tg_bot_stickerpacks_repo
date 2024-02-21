from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_buttons = [
    [InlineKeyboardButton(text='Создать пак', callback_data='create_stickerset_button')],
    [InlineKeyboardButton(text='Мои паки', callback_data='my_stickersets_button')]
]

menu_inline_kb = InlineKeyboardMarkup(inline_keyboard=menu_buttons)