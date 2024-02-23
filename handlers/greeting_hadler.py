from aiogram import Router
from aiogram.types import Message
from keyboards.start_menu_keyboard_keyboard import menu_inline_kb
from datetime import datetime
from aiogram.fsm.context import FSMContext

from database import session_factory
from models.user import UserORM
from sqlalchemy import select


router = Router()

@router.message()
async def greeting_hadler(message: Message, state: FSMContext):
    await message.answer(text='😊 <b>Выбери действие</b>', reply_markup=menu_inline_kb, parse_mode='HTML')
    await state.clear()
    user_id = message.from_user.id

    async with session_factory() as session:
        query = select(UserORM).filter(UserORM.tg_id == user_id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            new_user = UserORM(
                tg_id=user_id,
                join_date=datetime.utcnow()
            )
            session.add(new_user)
            await session.commit()



