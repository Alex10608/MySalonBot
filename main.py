import asyncio
import logging

from aiogram import Bot, Dispatcher

from keyboards.main_menu import set_main_menu
from handlers import user_handlers
from config.config import load_config
from handlers.user_handlers import storage


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')
    config = load_config('/config')

    bot = Bot(
        token=config.tg_bot.token
    )
    dp = Dispatcher(storage=storage)
    await set_main_menu(bot)

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
