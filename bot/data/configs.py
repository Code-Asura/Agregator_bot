# Чистые импорты
import os
import aiofiles
import asyncio

# Полные импорты
from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr
from ujson import loads
from aiogram.types import BotCommand
from typing import List

# Функция извлечения данных из json
async def get_json(filename: str) -> list:
    path = f"bot/data/json/{filename}.json"
    if os.path.exists(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as file:
            return loads(await file.read())
    return []

# Класс конфигурации
class SetConfig(BaseSettings):
    token: SecretStr
    commands: List = [BotCommand(command=cmd[0], description=cmd[1])
                       for cmd in asyncio.run(get_json("my_commands"))]

    model_config = SettingsConfigDict(env_file='bot/.env', env_file_encoding='utf-8')

# Экземпляр класса
config = SetConfig()