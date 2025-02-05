# Чистые импорты
import os
import asyncio
import logging

# Полные импорты
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Кастомные чистые импорты


# Кастомные полные импорты
from data import config
from handlers import setup_router

# Корневая функия
async def main():
    #Логирование 
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    logger.info("Бот запущен!")


    bot = Bot(config.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
            )
    
    dp = Dispatcher()

    router = setup_router()
    dp.include_router(router)

    #Запуск бота
    try:
        await bot.delete_webhook(True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# Проверка и запуск бота
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")