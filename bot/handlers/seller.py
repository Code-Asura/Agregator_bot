# Полные импорты
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data.configs import RegisterSeller, EditSeller

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
        await seller_true.send_msg(msg)
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
async def reg_seller_yes(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Сохраняю данные...")
    await db.seller_manager.register_seller(state)
    await call.message.answer("Данные сохранены")
    await call.message.answer("Вы зарегистрированы как продавец")
    await state.clear()

@router.callback_query(F.data == "no_reg_seller")
async def reg_seller_no(call: CallbackQuery):
    await no_reg_seller_menu.send_call_del(call)

@router.callback_query(F.data == "redacted_seller")
async def redacted_seller_func(call: CallbackQuery):
    await redacted_seller.send_call_del(call)

@router.callback_query(F.data == "edit_company_name")
async def edit_company_name(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название вашей компании")
    await state.set_state(EditSeller.company_name)

@router.message(EditSeller.company_name)
async def edit_company_name(msg: Message, state: FSMContext):
    await state.update_data(company_name=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Название компании изменено")
    await state.clear()

@router.callback_query(F.data == "edit_types")
async def edit_types(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите тип продукции")
    await state.set_state(EditSeller.types)

@router.message(EditSeller.types)
async def edit_types(msg: Message, state: FSMContext):
    await state.update_data(types=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Тип продукции изменен")
    await state.clear()

@router.callback_query(F.data == "edit_short_desc")
async def edit_short_desc(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите короткое описание")
    await state.set_state(EditSeller.short_desc)

@router.message(EditSeller.short_desc)
async def edit_short_desc(msg: Message, state: FSMContext):
    await state.update_data(short_desc=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Краткое описание изменено")
    await state.clear()

@router.callback_query(F.data == "edit_photo_id")
async def edit_photo_id(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пришлите новую фотографию")
    await state.set_state(EditSeller.photo_id)

@router.message(EditSeller.photo_id)
async def edit_photo_id(msg: Message, state: FSMContext):
    await state.update_data(photo_id=msg.photo[0].file_id)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Фотография изменена")
    await state.clear()

@router.callback_query(F.data == "edit_full_desk")
async def edit_full_desk(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите полное описание")
    await state.set_state(EditSeller.full_desc)

@router.message(EditSeller.full_desc)
async def edit_full_desk(msg: Message, state: FSMContext):
    await state.update_data(full_desc=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Полное описание изменено")
    await state.clear()

@router.callback_query(F.data == "full_edit_seller")
async def full_edit_seller(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название вашей компании")
    await state.set_state(RegisterSeller.company_name)

