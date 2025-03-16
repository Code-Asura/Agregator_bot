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
from aiogram.fsm.state import State, StatesGroup
from typing import List, Dict
from aiogram.fsm.state import State, StatesGroup

# region FSM
class RegisterSeller(StatesGroup):
    contact = State()
    company_name = State()
    types = State()
    short_desc = State()
    full_desc = State()
    photo_id = State()
    tg_id = State()

class EditSeller(StatesGroup):
    contact = State()
    company_name = State()
    types = State()
    short_desc = State()
    full_desc = State()
    photo_id = State()
    tg_id = State()
    message_id = State()

class Feedback(StatesGroup):
    message = State()
    photo = State()
# endregion

# Функция извлечения данных из json
async def get_json(filename: str) -> list:
    """Извлечение данных из json"""
    path = f"bot/data/json/{filename}.json"
    if os.path.exists(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as file:
            return loads(await file.read())
    return []

# Класс конфигурации
class SetConfig(BaseSettings):
    token: SecretStr
    db_url: str
    other_grup: int
    feedback_thread: int
    confirming_thread: int
    superadmin: List = [i for i in asyncio.run(get_json("superadmin"))]
    commands: List = [BotCommand(command=cmd[0], description=cmd[1])
                       for cmd in asyncio.run(get_json("my_commands"))]

    model_config = SettingsConfigDict(env_file='bot/.env', env_file_encoding='utf-8')

# Экземпляр класса
config = SetConfig()