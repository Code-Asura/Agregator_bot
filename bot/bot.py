# Чистые импорты
import asyncio
import logging

# Полные импорты
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Кастомные полные импорты
from data import config
from handlers import setup_router
from data.database import DBConnect

# Корневая функия
async def main():
    #Логирование 
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(message)s",
    )

    logger.error("Бот запущен!")

    # Определение бота
    bot = Bot(config.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
            )
    # Подключение меню команд
    await bot.set_my_commands(config.commands)
    
    # Регистрация хранилища состояний
    storage = MemoryStorage()

    # Определение диспечера
    dp = Dispatcher(storage=storage)

    # Подключение обработчиков (роутеров)
    router = setup_router()
    dp.include_router(router)

    # Проверка базы данных
    await DBConnect.init_db()
    
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
        