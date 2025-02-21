# Полные импорты
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data.configs import RegisterSeller

# Импорт класса работы с базой данных
from data.database import DBConnect

# Импорт всех экземпляров для отправки сообщений
from utils.seller_lexicon import *

# Экземпляр класса обработчика
router = Router()
# Экземпляр класса БД
db = DBConnect()

@router.message(Command('reg_seller'))
async def reg_seller(msg: Message, state: FSMContext):
    if await db.seller_manager.check_seller(msg.from_user.id):
        await msg.answer("Вы уже зарегистрированы как продавец")
        return
    await msg.answer("Вы перешли в раздел <b>Регистрация продавца</b>")
    await msg.answer("Введите название вашей компании")
    await state.set_state(RegisterSeller.company_name)


@router.message(RegisterSeller.company_name)
async def company_name(msg: Message, state: FSMContext):
    await state.update_data(company_name=msg.text)
    await msg.answer("Выберите тип продукции")
    await state.set_state(RegisterSeller.types)

@router.message(RegisterSeller.types)
async def types(msg: Message, state: FSMContext):
    await state.update_data(types=msg.text)
    await msg.answer("Введите короткое описание продукции")
    await state.set_state(RegisterSeller.short_desc)

@router.message(RegisterSeller.short_desc)
async def short_desc(msg: Message, state: FSMContext):
    await state.update_data(short_desc=msg.text)
    await msg.answer("Введите полное описание продукции")
    await state.set_state(RegisterSeller.full_desc)

@router.message(RegisterSeller.full_desc)
async def full_desc(msg: Message, state: FSMContext):
    await state.update_data(full_desc=msg.text)
    await msg.answer("Пришлите фотографию продукции")
    await state.set_state(RegisterSeller.photo_id)

@router.message(RegisterSeller.photo_id)
async def photo_id(msg: Message, state: FSMContext):
    await state.update_data(photo_id=msg.photo[0].file_id)
    await state.update_data(tg_id=msg.from_user.id)
    data = await state.get_data()
    await msg.answer_photo(
        photo=data['photo_id'],
        caption=
        f"<b>Компания:</b> {data['company_name']}\n"
        f"<b>Тип продукции:</b> {data['types']}\n"
        f"<b>Короткое описание:</b> {data['short_desc']}\n"
        f"<b>Полное описание:</b> {data['full_desc']}\n"
)   
    await seller_reg_menu.send_msg(msg)

@router.callback_query(F.data == "yes_reg_seller")
async def reg_seller(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Сохраняю данные...")
    await db.seller_manager.register_seller(state)
    await call.message.answer("Данные сохранены")
    await call.message.answer("Вы зарегистрированы как продавец")
    await state.clear()
    