from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql import select, update, delete, exists
from sqlalchemy.orm import declarative_base, relationship, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, String, Table, MetaData,\
        ForeignKey, JSON, Text, BigInteger
from aiogram.fsm.context import FSMContext
from enum import Enum
from . import config

# Базовый класс декларативных моделей
Base = declarative_base()

#Перечисление ролей 
class Roles(Enum):
    USER = "user"
    SELLER = "seller"
    ADMIN = "admin"

# Модель для пользователей
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default=Roles.USER.value, index=True)
    seller = relationship("Seller", back_populates="users", uselist=False)

# Модель для продавцов 
class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    types = Column(String, nullable=False)
    photo_id = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    full_desc = Column(Text, nullable=False)
    users = relationship("Users", back_populates="seller")


class DBConnect:
    """Класс с подключением к БД"""

    engine = create_async_engine(url=config.db_url)
    session = async_sessionmaker(engine,expire_on_commit=False)

    def __init__(self):
        self.user_manager = self.UserManager(self)
        self.seller_manager = self.SellerManager(self)
    
    @classmethod
    async def init_db(cls):
        """Проверка существуют ли таблицы и их создание если нет"""
        async with cls.engine.begin() as conn:
            print("Проверка/создание таблиц...")
            await conn.run_sync(Base.metadata.create_all)
            print("Проверка/создание таблиц завешено")

    async def select_data(self, table: str, param: str, arg: str):
        """Извлечение данных с БД"""
        async with self.session() as session:
            result = await session.execute(select(table).filter_by(param=arg))
            return result.scalars().first()
        
    class UserManager:
        """Класс управления пользователями"""
        def __init__(self, outer_self):
            self.session = outer_self.session
        
        async def _check_user(self, tg_id) -> bool:
            query = select(exists().where(Users.tg_id == tg_id))
            result = await self.session.execute(query)
            return result.scalar()

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
            async with self.session() as session:
                try:
                    new_user = Users(
                        tg_id=tg_id,
                        username=username,
                        name=name
                    )
                    session.add(new_user)
                    await session.commit()

                    if username is not None:
                        print(f"Пользователь {username} добавлен")
                    else:
                        print(f"Пользователь {name} с id:{tg_id} добавлен")

                except IntegrityError:
                    if username is not None:
                        print(f"Пользователь {username} уже существует")
                    else:
                        print(f"Пользователь {name} с id:{tg_id} уже существует")
                        
                except Exception as e:
                    print(type(e).__name__)
                

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
        def __init__(self, outer_self):
            self.session = outer_self.session

        async def check_seller(self, tg_id) -> bool:
            async with self.session() as session:
                query = select(Users).where(Users.tg_id == tg_id)
                result = await session.execute(query)
                user = result.scalars().first()

                if user.role == Roles.SELLER.value:
                    if user.username is not None:
                        print(f"Продавец {user.username} уже зарегистрирован")
                    else:
                        print(f"Продавец {user.name} с id:{user.tg_id} зарегистрирован")

                return True

        async def register_seller(self, state: FSMContext):
            """Регистрация продавца"""
            async with self.session() as session:
                data = await state.get_data()

                stmt = select(Users).where(Users.tg_id == data["tg_id"])
                result = await session.execute(stmt)
                user = result.scalars().first()

                user.role = Roles.SELLER.value

                new_seller = Seller(
                    user_id=user.id,
                    types=data["types"],
                    photo_id=data["photo_id"],
                    company_name=data["company_name"],
                    short_desc=data["short_desc"],
                    full_desc=data["full_desc"]
                )
                session.add(new_seller)
                await session.commit()

                if user.username is not None:
                    print(f"Продавец {user.username} зарегистрирован")
                else:
                    print(f"Продавец {user.name} с id:{user.tg_id} зарегистрирован")
                    


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
