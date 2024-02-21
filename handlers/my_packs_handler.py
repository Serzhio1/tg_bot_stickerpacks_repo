from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy import select, delete
from database import session_factory
from models.user_stickersets import UserStickersetsORM
from keyboards.user_stickersets_list_keyboard import user_stickerset_list
from states import CreateStickerset
from keyboards.stickerset_actions_list_keyboard import stickerset_actions_list_kb
from keyboards.confirm_delete_stickerset_keyboard import confirm_delete_stickerset_kb
from keyboards.start_menu_keyboard_keyboard import menu_inline_kb


router = Router()

def correct_date_format(num: int) -> str:
    if num >= 10:
        return num
    else:
        return f"0{num}"

@router.callback_query(F.data=='back_to_menu_button')
async def back_menu_processing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='😃 <b>Выбери действие</b>', reply_markup=menu_inline_kb, parse_mode='HTML')
    await state.clear()

@router.callback_query(F.data == 'delete_stickerset')
async def intention_delete_stickerset(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('😥 <b>Точно хотите удалить стикерпак?</b>', reply_markup=confirm_delete_stickerset_kb, parse_mode='HTML')

@router.callback_query(F.data == 'cancel_button')
async def cancel_processing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='😃 <b>Выбери действие</b>', reply_markup=menu_inline_kb, parse_mode='HTML')
    await state.clear()

@router.callback_query(F.data == 'delete_stickerset_button')
async def delete_stickerset(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    stickerset_name = data.get('edit_stickerset_name')
    await bot.delete_sticker_set(name=stickerset_name)
    async with session_factory() as session:
        query = delete(UserStickersetsORM).where(UserStickersetsORM.stickerset_name == stickerset_name)
        await session.execute(query)
        await session.commit()
    await callback.message.answer(text='<b>Cтикерпак был успешно удален</b>', parse_mode='HTML')
    await callback.message.edit_text(text='😃 <b>Выбери действие</b>', reply_markup=menu_inline_kb, parse_mode='HTML')
    await state.clear()

@router.callback_query(F.data=='my_stickersets_button')
async def see_my_packs(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.message.edit_text(text='👇<b>Выбери нужный стикерпак</b>👇', reply_markup=await user_stickerset_list(user_id=user_id), parse_mode='HTML')
    await state.set_state(CreateStickerset.choosing_stickerset)

@router.callback_query(CreateStickerset.choosing_stickerset)
async def stickerset_actions_list(callback: CallbackQuery, state: FSMContext):
    async with session_factory() as session:
        query = select(UserStickersetsORM).filter(UserStickersetsORM.stickerset_name == callback.data)
        result = await session.execute(query)
        stickerset = result.scalar()
    stickerset_date_added = stickerset.date_added
    stickerset_name = stickerset.title

    await callback.message.edit_text(text=(
        '<b>Инфа про твой пак:</b>\n\n'
        f'🆔 <b>Название:</b> {stickerset_name.split("@")[0][:-1]}\n'
        f'🕓 <b>Дата создания:</b> {correct_date_format(stickerset_date_added.day)}.{correct_date_format(stickerset_date_added.month)}.{stickerset_date_added.year}\n'
        f'🔗 <b>Ссылка на стикерпак:</b> https://t.me/addstickers/{callback.data}\n'),
        reply_markup=stickerset_actions_list_kb,
        parse_mode='HTML')
    await state.update_data(edit_stickerset_name=callback.data)
    await state.set_state(CreateStickerset.adding_sticker_to_stickerset)

@router.callback_query(CreateStickerset.adding_sticker_to_stickerset)
async def add_sticker_to_stickerset(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_new_stickerset=False)
    await callback.message.edit_text(text='🌈 <b>Отправь картинку, которую хочешь добавить в этот стикерсет</b>', parse_mode='HTML')
    await state.set_state(CreateStickerset.stickers_input)




