from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, InputSticker, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.actions_after_creating_stickerset_keyboard import actions_after_creating_stickerset_kb
from states import CreateStickerset
from random import randint
from asyncio import sleep
import asyncio
import os
from transliterate import translit

from database import session_factory
from models.user_stickersets import UserStickersetsORM


router = Router()

def random_long_number():
    return randint(10000000, 99999999)

async def get_bot_name(bot: Bot):
    info_about_bot = await bot.me()
    bot_name = info_about_bot.username
    return bot_name


async def convert_to_png(input_file: str) -> str:
    file_path, ext = input_file.rsplit(".", 1)
    output_file = f"{file_path}.out.{ext}"
    r = await asyncio.subprocess.create_subprocess_exec(
        *["ffmpeg", "-v", "0", "-y", "-i", input_file, "-vf", "scale=512:512", output_file])
    await r.wait()
    return output_file

# the user clicked on the "create stickerset" button in the menu
@router.callback_query(F.data == 'create_stickerset_button')
async def start_create_new_stickerset(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='<b>Введите название для стикерпака</b>', parse_mode='HTML')
    await state.set_state(CreateStickerset.stickerset_input_title)

# the user enters a name for the new stickerset
@router.message(CreateStickerset.stickerset_input_title)
async def stickerset_title_verification(message: Message, state: FSMContext, bot: Bot):
    bot_name = await get_bot_name(bot=bot)
    stickerset_title = message.text
    stickerset_name = translit(value=stickerset_title, language_code='ru', reversed=True).replace(" ", "_").lower( )
    #print(f'{stickerset_name}_by_{bot_name}')
    #print(f'{translit(value=stickerset_title, language_code="ru", reversed=True)}_by_{bot_name}')
    if len(stickerset_title + bot_name) + 2 > 64:
        await message.answer(text=(
            'Вы ввели слишком длинное название для стикерпака.'
            'Попробуйте еще раз'))
    else:
        await state.set_data({
            "create_stickerset": True,
            "stickerset_title": f'{stickerset_title} @{bot_name}', # TODO сделать транслитирование title -> name
            "stickerset_name": f'{stickerset_name}_by_{bot_name}'
        })
        await message.answer(text=(
            '<b>Отлично! Теперь делаем так:</b>\n\n'
            '<b>1.</b> Отсправь мне <b>картинку</b> и я сразу добавляю ее в новый стикерпак с эмодзи 🌟\n'
            '<b>2.</b> Отправь мне <b>эмодзи</b>, если хочешь назначить его предыдущему стикеру\n'
            '<b>3.</b> Процесс добавления стикеров будет повторяться до тех пор, пока ты не нажмешь кнопку <b>«Готово»</b>\n\n'),
            parse_mode='HTML')
        await sleep(1.5)
        await message.answer(text='Давай начнем! Отправь мне первую картинку🖼')
        await state.set_state(CreateStickerset.sending_image)

@router.message(CreateStickerset.sending_image)
async def get_image(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    # we check if the user sent a photo or something else
    if message.photo == None:
        await message.answer(text=(
            'Кажатся, вы отправили не картинку, а что-то другое...😬\n'
            'Попробуйте еще раз!)'))
    else:
        # collect information about the file
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        info_about_file = await bot.get_file(file_id)
        file_path = info_about_file.file_path
        file_extension = file_path.rsplit('.', 1)[-1]

        # to function in utils module
        # TODO check if is already capable and pass conversation
        # converting the file to png format
        download_file = f"output{file_unique_id}.{file_extension}"
        await bot.download_file(file_path=file_path, destination=download_file)

        image_png = await convert_to_png(download_file)
        # till here
        sticker_input_file = FSInputFile(image_png)
        # creating a sticker as an instance of the InputSticker class

        upload_sticker_file = await bot.upload_sticker_file(user_id=user_id, sticker=sticker_input_file, sticker_format='static')
        os.remove(download_file)

        sticker_id = upload_sticker_file.file_id
        sticker = InputSticker(sticker=sticker_id, emoji_list=list('🌟'))

        #await state.update_data(last_added_sticker=sticker_id)
        data = await state.get_data()
        stickerset_title = data.get('stickerset_title')
        stickerset_name = data.get('stickerset_name')

        await bot.create_new_sticker_set(
            user_id=user_id,
            name=stickerset_name,
            title=stickerset_title,
            stickers=[sticker],
            sticker_format='static')

        async with session_factory() as session:
            new_stickerset = UserStickersetsORM(
                stickerset_name=stickerset_name,
                tg_id=user_id,
                title=stickerset_title,
            )
            session.add(new_stickerset)
            await session.commit()

        await message.answer(text=(
            '🌈 <b>Отлично, стикер добавлен!</b>\n\n'
            '<b>1.</b> Отправь следующую <b>картинку</b>, чтобы добавить еще один стикер в этот стикерпак\n'
            '<b>2.</b> Отправь <b>эмодзи</b>, если хочешь назначить его предыдущему стикеру\n'
            '<b>3.</b> Нажми кнопку <b>"Готово"</b>, если хочешь закончить работу с этим стикерпаком'),
            reply_markup=actions_after_creating_stickerset_kb,
            parse_mode='HTML')
        await state.set_state(CreateStickerset.stickers_input)




