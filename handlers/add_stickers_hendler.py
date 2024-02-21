from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, InputSticker, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from keyboards.actions_after_creating_stickerset_keyboard import actions_after_creating_stickerset_kb
from aiogram.fsm.context import FSMContext
from states import CreateStickerset
import os

from handlers.create_stickerset_handler import convert_to_png
router = Router()

#def convert_to_png(file_path, file_unique_id, bot):
#    file_extension = file_path.rsplit('.', 1)[-1]
#    download_file = f"output.{file_extension}"
#    #await bot.download_file(file_path=file_path, destination=download_file)
#    image_png = f'images/{file_unique_id}.png'
#    subprocess.call(["ffmpeg", "-v", "0", "-y", "-i", download_file, "-vf", "scale=512:512", image_png])
#    os.remove(download_file)
#    return image_png

@router.message(CreateStickerset.stickers_input)
async def add_sticker_to_stickerset(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    image = message.photo
    emoji = message.text

    data = await state.get_data()
    is_newly_created_stickerset = data.get('create_stickerset')

    if image != None: # add another one sticker to current stickerset
        if is_newly_created_stickerset: # if we are working with a stickerset that has just been created, then we know the name of this stickerset because it lies in the state
            stickerset_name = data.get('stickerset_name')
            await state.update_data(is_new_stickerset=False)
            file_id = message.photo[-1].file_id
            file_unique_id = message.photo[-1].file_unique_id
            info_about_file = await bot.get_file(file_id)
            file_path = info_about_file.file_path
            file_extension = file_path.rsplit('.', 1)[-1]

            download_file = f"output{file_unique_id}.{file_extension}"
            await bot.download_file(file_path=file_path, destination=download_file)

            image_png = await convert_to_png(download_file)
            # create_sticker_from_image_png
            sticker_input_file = FSInputFile(image_png)

            upload_sticker_file = await bot.upload_sticker_file(user_id=user_id, sticker=sticker_input_file, sticker_format='static')
            os.remove(download_file)
            sticker_id = upload_sticker_file.file_id
            sticker = InputSticker(sticker=sticker_id, emoji_list=list('🌟'))

            await bot.add_sticker_to_set(user_id=user_id, name=stickerset_name, sticker=sticker)
            await state.update_data(last_added_sticker=sticker_id)
            await message.answer(text=(
                '🌈 <b>Отлично, стикер добавлен в этот же стикерпак!</b>\n\n'
                '<b>1.</b> Отправь следующую <b>картинку</b>, чтобы добавить еще один стикер в этот стикерпак\n'
                '<b>2.</b> Отправь <b>эмодзи</b>, если хочешь назначить его предыдущему стикеру\n'
                '<b>3.</b> Нажми кнопку <b>"Готово"</b>, если хочешь закончить работу с этим стикерпаком'),
                reply_markup=actions_after_creating_stickerset_kb,
                parse_mode='HTML')

        else: #add a sticker not to the newly created sticker set
            stickerset_name = data.get('edit_stickerset_name')
            file_id = message.photo[-1].file_id
            file_unique_id = message.photo[-1].file_unique_id
            info_about_file = await bot.get_file(file_id)
            file_path = info_about_file.file_path
            file_extension = file_path.rsplit('.', 1)[-1]

            download_file = f"output{file_unique_id}.{file_extension}"
            await bot.download_file(file_path=file_path, destination=download_file)

            image_png = await convert_to_png(download_file)

            # create_sticker_from_image_png
            sticker_input_file = FSInputFile(image_png)

            upload_sticker_file = await bot.upload_sticker_file(user_id=user_id, sticker=sticker_input_file, sticker_format='static')
            os.remove(image_png)
            sticker_id = upload_sticker_file.file_id
            sticker = InputSticker(sticker=sticker_id, emoji_list=list('🌟'))
            await bot.add_sticker_to_set(user_id=user_id, name=stickerset_name, sticker=sticker)
            await state.update_data(last_added_sticker=sticker_id)
            await message.answer(text=(
                '🌈 <b>Отлично, стикер добавлен!</b>\n\n'
                '<b>1.</b> Отправь следующую <b>картинку</b>, чтобы добавить еще один стикер в этот стикерпак\n'
                '<b>2.</b> Отправь <b>эмодзи</b>, если хочешь назначить его предыдущему стикеру\n'
                '<b>3.</b> Нажми кнопку <b>"Готово"</b>, если хочешь закончить работу с этим стикерпаком'),
                reply_markup=actions_after_creating_stickerset_kb,
                parse_mode='HTML')

    else: # we put the emoji in accordance with the previous picture
        data = await state.get_data()
        stickerset_name = data.get('stickerset_name')
        info_about_stickerset = await bot.get_sticker_set(stickerset_name)
        print(info_about_stickerset)
        last_sticker_id = info_about_stickerset.stickers[-1].file_id
        await bot.set_sticker_emoji_list(sticker=last_sticker_id, emoji_list=list(emoji))

        #last_added_sticker = state.update_data(last_sticker_id=last_sticker_id)
        await message.answer(text=(
            f'🌈 <b>Отлично, эмодзи {emoji} назначен предыдущему стикеру!</b>\n\n'
            '<b>1.</b> Отправь следующую <b>картинку</b>, чтобы добавить еще один стикер в этот стикерпак\n'
            '<b>2.</b> Отправь <b>эмодзи</b>, если хочешь назначить его предыдущему стикеру\n'
            '<b>3.</b> Нажми кнопку <b>"Готово"</b>, если хочешь закончить работу с этим стикерпаком'),
            reply_markup=actions_after_creating_stickerset_kb,
            parse_mode='HTML')




