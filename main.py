import asyncio
from aiogram import Bot, Dispatcher
from handlers import greeting_hadler
from handlers import create_stickerset_handler
from handlers import add_stickers_hendler
from handlers import finish_work_with_stickerset_handler
from handlers import my_packs_handler

from database import async_engine, Base
from models import *
import config



async def main():
    bot = Bot(token='6492750183:AAHmx4Yk5hG9ZD8uPJyS94UmTpi6tW18ulc')
    dp = Dispatcher()

    async with async_engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    dp.include_router(create_stickerset_handler.router)
    dp.include_router(add_stickers_hendler.router)
    dp.include_router(finish_work_with_stickerset_handler.router)
    dp.include_router(greeting_hadler.router)
    dp.include_router(my_packs_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())