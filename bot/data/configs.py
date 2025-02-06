import os

from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr

# Класс конфигурации
class SetConfig(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(env_file='bot/.env', env_file_encoding='utf-8')

# Экземпляр класса
config = SetConfig()