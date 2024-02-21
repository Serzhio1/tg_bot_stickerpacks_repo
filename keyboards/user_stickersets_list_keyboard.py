from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import session_factory
from models.user_stickersets import UserStickersetsORM
from sqlalchemy import select

async def user_stickerset_list(user_id):
    user_stickerset_list_buttons = []
    async with session_factory() as session:
        query = select(UserStickersetsORM).filter(UserStickersetsORM.tg_id == user_id)
        result = await session.execute(query)
        user_stickerpacks = result.scalars().all()
        count_stickerpacks = 0
        for stickerpack in user_stickerpacks:
            count_stickerpacks += 1
            user_stickerset_list_buttons.append(
                [InlineKeyboardButton(text=f'{stickerpack.title.split("@")[0][:-1]}', callback_data=f'{stickerpack.stickerset_name}')]
            )
        user_stickerset_list_buttons.append(
            [InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_menu_button')]
        )
        user_stickerset_list_kb = InlineKeyboardMarkup(inline_keyboard=user_stickerset_list_buttons)
    return user_stickerset_list_kb