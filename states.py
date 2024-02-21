from aiogram.fsm.state import State, StatesGroup

class CreateStickerset(StatesGroup):
    stickerset_input_title = State()
    sending_image = State()
    sendind_another_one_image = State()
    waiting_link_stickerset = State()
    stickers_input = State()
    choosing_stickerset = State()
    adding_sticker_to_stickerset = State()

