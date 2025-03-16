from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.orm import declarative_base, relationship, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import Column, Integer, String, ForeignKey, Text, BigInteger, func

from aiogram.fsm.context import FSMContext
from enum import Enum

from . import config

# Базовый класс декларативных моделей
Base = declarative_base()

# region Модели
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
    contact = Column(String, nullable=False)
    types = Column(String, nullable=False)
    photo_id = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    full_desc = Column(Text, nullable=False)
    users = relationship("Users", back_populates="seller")

class TimedStorage(Base):
    __tablename__ = "timed_storage"
    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    contact = Column(String, nullable=False)
    types = Column(String, nullable=False)
    photo_id = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    full_desc = Column(Text, nullable=False)
# endregion

# region Работа с БД
class DBConnect:
    """Класс с подключением к БД"""

    engine = create_async_engine(url=config.db_url)
    session = async_sessionmaker(engine,expire_on_commit=False)

    def __init__(self):
        self.user_manager = self.UserManager(self)
        self.seller_manager = self.SellerManager(self)
        self.time_storage = self.TimeStorage(self)
    
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
    # region Работа с юзером
    class UserManager:
        """Класс управления пользователями"""
        def __init__(self, outer_self):
            self.session = outer_self.session

        async def add_right(self, role_name):
            """Добавление ролей"""
            #TODO {отложено} Логика добавлений прав
            pass

        async def modify_right(self, role_name):
            """Изменение ролей"""
            #TODO {отложено} Логика изменения прав
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
                    pass
                        
                except Exception as e:
                    print(type(e).__name__)
                
        async def modify_user(self, tg_id, username, name):
            """Изменение данных пользователя"""
            async with self.session() as session:
                try:
                    result = await session.execute(
                        select(Users).where(Users.tg_id == tg_id)
                    )
                    user = result.scalar_one_or_none()
                    
                    if user:
                        if user.username != username or user.name != name:
                            user.username = username
                            user.name = name
                            await session.commit()
                            print(f"Пользователь {tg_id} обновлен")
                        else:
                            print("Данные пользователя не изменились")
                    else:
                        print(f"Пользователь с tg_id {tg_id} не найден")
                
                except SQLAlchemyError as e:
                    print(f"Ошибка базы данных: {e}")
    # endregion
    # region Работа с селлером
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
                else:
                    return False
        async def register_seller(self, state: FSMContext):
            """Регистрация продавца"""
            async with self.session() as session:
                data = await state.get_data()

                stmt = select(Users).where(Users.tg_id == data["tg_id"])
                result = await session.execute(stmt)
                user = result.scalars().first()
                
                if user.role == Roles.SELLER.value:
                    stmt = select(Seller).where(Seller.user_id == user.id)
                    result = await session.execute(stmt)
                    seller = result.scalars().first()
                    
                    seller.contact = data['contact']
                    seller.company_name = data["company_name"]
                    seller.types=data["types"]
                    seller.photo_id=data["photo_id"]
                    seller.short_desc=data["short_desc"]
                    seller.full_desc=data["full_desc"]

                    await session.commit()

                    return

                user.role = Roles.SELLER.value

                new_seller = Seller(
                    user_id=user.id,
                    contact=data['contact'],
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
                    
        async def edit_seller(self, state: FSMContext):
            """Изменение данных продавца с проверкой"""
            async with self.session() as session:
                data = await state.get_data()

                result = await session.execute(
                        select(Users).options(joinedload(Users.seller)).
                        filter(Users.tg_id == data['tg_id'])
                    )
                
                user = result.scalars().first()
                seller = user.seller

                match data:
                    case {"company_name": company_name}:
                        seller.company_name = company_name
                    case {"short_desc": short_desc}:
                        seller.short_desc = short_desc
                    case {"full_desc": full_desc}:
                        seller.full_desc = full_desc
                    case {"photo_id": photo_id}:
                        seller.photo_id = photo_id
                    case {"types": types}:
                        seller.types = types
                    case {"contact": contact}:
                        seller.contact = contact
                    case _:
                        return False

                await session.commit()

                if user.username is not None:
                    print(f"Продавец {user.username} изменен")
                else:
                    print(f"Продавец {user.name} с id:{user.tg_id} изменен")

        async def select_info(self, types, options=None):
            """Извлечение данных по типу для покупателей с подгрузкой данных о пользователе"""
            async with self.session() as session:
                query = (
                    select(Seller)
                    .where(Seller.types == types)
                    .order_by(func.random())
                    .limit(5)
                    .options(joinedload(Seller.users))  # Загрузка связанных данных о пользователе
                )
                result = await session.execute(query)
                sellers = result.scalars().all()
                return sellers

        async def get_seller_by_id(self, seller_id: int) -> Seller:
            async with self.session() as session:
                stmt = select(Seller).where(Seller.id == seller_id).options(joinedload(Seller.users))
                result = await session.execute(stmt)
                return result.scalars().first()
    # endregion

    class TimeStorage:
        def __init__(self, outer_self):
            self.session = outer_self.session

        async def add_timed_data(self, state: FSMContext):
            async with self.session() as session:
                data = await state.get_data()

                new_row = TimedStorage(
                        chat_id = data['tg_id'],
                        message_id = data['message_id'],
                        contact = data['contact'],
                        types = data['types'],
                        photo_id = data['photo_id'],
                        company_name = data['company_name'],
                        short_desc = data['short_desc'],
                        full_desc = data['full_desc']
                )
                session.add(new_row)
                await session.commit()

                print("+ временные данные")
        
        async def get_timed_data(self, msg_id):
            async with self.session() as session:
                query = await session.execute(select(TimedStorage)
                                             .where(TimedStorage.message_id == msg_id))
                data = query.scalars().first()

                stmt = select(Users).where(Users.tg_id == data.chat_id)
                result = await session.execute(stmt)
                user = result.scalars().first()

                user.role = Roles.SELLER.value

                new_seller = Seller(
                    user_id=user.id,
                    contact=data.contact,
                    types=data.types,
                    photo_id=data.photo_id,
                    company_name=data.company_name,
                    short_desc=data.short_desc,
                    full_desc=data.full_desc
                )
                session.add(new_seller)

                if user.username is not None:
                    print(f"Продавец {user.username} зарегистрирован")
                else:
                    print(f"Продавец {user.name} с id:{user.tg_id} зарегистрирован")
                
                await session.delete(data)

                await session.commit()


                print("- временные данные")
                return data
        
        async def delete_timed_data(self, msg_id):
            async with self.session() as session:
                query = await session.execute(select(TimedStorage)
                                             .where(TimedStorage.message_id == msg_id))
                data = query.scalars().first()

                await session.delete(data)
                await session.commit()
                
                print("- временные данные")
                return data
# endregion
