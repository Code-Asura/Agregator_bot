from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, MetaData,\
        ForeignKey, JSON, Text

# Базовый класс декларативных моделей
Base = declarative_base()

# Модель для пользователей
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")

# Модель для продавцов 
class Seller:
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True)
    types = Column(String, nullable=False)
    photo_id = Column(Integer, nullable=False)
    company_name = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    full_desc = Column(Text, nullable=False)


class DBConnect:
    """Класс с подключением к БД"""
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url)
        self.session = sessionmaker(
            self.engine, expire_on_commit=False, class_= AsyncSession)

    async def select_data(self, table):
        """Извлечение данных с БД"""
        async with self.session() as session:
            result = await session.execute(select(table))
            return result.scalars().all()

    class UserManager:
        """Класс управления пользователями"""
        def __init__(self, session):
            self.session = session
        
        async def add_right(self, role_name):
            """Добавление ролей"""
            #TODO Логика добавлений прав
            pass

        async def remove_right(self, role_name):
            """Удаление ролей"""
            #TODO Логика удаления прав
            pass

        async def modify_right(self, role_name):
            """Изменение ролей"""
            #TODO Логика изменения прав
            pass

        async def add_user(self, tg_id, username, name):
            """Добавление пользователя"""
            #TODO Логика добавлений пользователя
            pass

        async def remove_user(self, tg_id, username, name):
            """Удаление пользователя"""
            #TODO Логика удаления пользователя
            pass

        async def modify_user(self, tg_id, username, name):
            """Изменение данных пользователя"""
            #TODO Логика изменения пользователя
            pass

        async def select_role(self, role_name, tg_id):
            """Извлечение роли пользователя для фильтра"""
            #TODO Логика извлечения роли пользователя
            pass

        async def select_user(self, tg_id):
            pass

    class SellerManager:
        """Класс управления данными продавцов"""
        def __init__(self, session):
            self.session = session

        async def add_info(self, item_type, item_details, item_photo_id):
            """Добавление данных"""
            #TODO Логика добавлений товара или услуги
            pass

        async def modify_info(self, item_type, item_details, item_photo_id):
            """Изменение данных"""
            #TODO Логика изменения товара или услуги
            pass

        async def select_info(self, types):
            """Извлечение данных по типу для покупателей"""
            #TODO Логика извлечения данных по типу
            pass

        