from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.start_menu_keyboard_keyboard import menu_inline_kb


router = Router()

@router.callback_query(F.data == 'done_button')
async def finish_work_with_current_stickerset(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    stickerset_name = data.get('stickerset_name')
    await callback.message.edit_text(text=(
        '😊 <b>Отлично! Работа со стикерпаком завершена</b>\n\n'
        f'👇 <b>Лови ссылку: </b> https://t.me/addstickers/{stickerset_name}'),
        reply_markup=menu_inline_kb,
        parse_mode='HTML')
    await state.clear()

