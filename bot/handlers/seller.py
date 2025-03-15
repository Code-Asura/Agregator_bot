#Системные импорты
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder as IKB
from data import config
# Импорт классов состояний
from data.configs import RegisterSeller, EditSeller

# Импорт класса работы с базой данных
from data.database import DBConnect

# Импорт всех экземпляров для отправки сообщений
from utils.seller_lexicon import *
from utils.buyer_lexicon import main_menu

router = Router() # Экземпляр класса обработчика
db = DBConnect() # Экземпляр класса БД

# region Регистрация
# Обработчик команды регистрации продавца
@router.message(Command('reg_seller'))
async def reg_seller(msg: Message, state: FSMContext):
    # Проверка есть ли продавец в базе
    if await db.seller_manager.check_seller(msg.from_user.id):
        await seller_true.send_msg(msg)
    else:
        await seller_start_reg.send_msg(msg)
        await state.set_state(RegisterSeller.company_name)

# Обработчик состояния для имени компаннии
@router.message(RegisterSeller.company_name)
async def company_name(msg: Message, state: FSMContext):
    ikb = IKB()
    ikb.button(text="Да", callback_data="yes_reg_company_name")
    ikb.button(text="Нет", callback_data="no_reg_company_name")
    await state.update_data(tg_id=msg.from_user.id)
    await state.update_data(company_name=msg.text)
    await msg.answer(f"Ваше название {msg.text}?", reply_markup=ikb.as_markup())

@router.callback_query(F.data == "yes_reg_company_name")
async def yes_reg_company_name_func(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите тип продукции")
    await reg_seller_types_menu.send_call(call)
    await state.set_state(RegisterSeller.types)

@router.callback_query(F.data == "no_reg_company_name")
async def no_reg_company_name_func(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название компании")
    await state.set_state(RegisterSeller.company_name)

@router.callback_query(F.data == "food_reg_seller")
async def food_reg_seller_func(call: CallbackQuery, state: FSMContext):
    await reg_seller_food_type_menu.send_call_del(call)


@router.callback_query(F.data.startswith("reg_seller_"))
async def reg_seller_ready_made_food_func(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    types = "_".join(call.data.split("_")[2:])
    match types:
        case "ready_made_food" | "meat_products" | "semi_finished" | \
             "desserts_pastries" | "diet_food" | "konc_sous_food" | "drinks":
            
            await state.update_data(types=types)
            await call.message.answer("Введите короткое описание")
            await state.set_state(RegisterSeller.short_desc)
        case "back_food":
            await yes_reg_company_name_func(call, state)

# Обработчик состояния для короткого описания
@router.message(RegisterSeller.short_desc)
async def short_desc(msg: Message, state: FSMContext):
    if msg.photo:
        await msg.answer("Короткое описание состоит из БУКВ и СЛОВ")
        state.set_state(RegisterSeller.short_desc)
        return
    await state.update_data(short_desc=msg.text)
    await msg.answer("Введите полное описание продукции")
    await state.set_state(RegisterSeller.full_desc)

# Обработчик состояния для полного описания
@router.message(RegisterSeller.full_desc)
async def full_desc(msg: Message, state: FSMContext):
    if msg.photo:
        await msg.answer("Полное описание состоит из БУКВ и СЛОВ")
        state.set_state(RegisterSeller.full_desc)
        return
    await state.update_data(full_desc=msg.text)
    await msg.answer("Пришлите фотографию продукции")
    await state.set_state(RegisterSeller.photo_id)

# Обработчик состояния для фотографии
#TODO {отложено} Доделать возможность принимать несколько фото и 1 для карточки
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

# Обработчик подтверждения на сохранение
@router.callback_query(F.data == "yes_reg_seller")
async def reg_seller_yes(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()

    ikb = IKB()
    ikb.button(text="Утвердить", callback_data="confirm")
    ikb.button(text="Отклонить", callback_data="cancell")

    mess = await call.bot.send_photo(
        chat_id=config.other_grup,
        photo=data['photo_id'],
        caption=
        f"<b>Компания:</b> {data['company_name']}\n"
        f"<b>Тип продукции:</b> {data['types']}\n"
        f"<b>Короткое описание:</b> {data['short_desc']}\n"
        f"<b>Полное описание:</b> {data['full_desc']}\n",
        message_thread_id=config.confirming_thread,
        reply_markup=ikb.as_markup()
    )
    await state.update_data(message_id=mess.message_id) 

    await db.time_storage.add_timed_data(state)

    await call.message.answer("Данные отправлены на проверку")

@router.callback_query(F.data == "confirm")
async def confirm_func(call: CallbackQuery):
    ikb = IKB()
    ikb.button(text="Главное меню", callback_data="main_menu")

    data = await db.time_storage.get_timed_data(call.message.message_id)
    await call.message.answer("Данные утверждены. Уведомление продавцу отправлено!")
    await call.bot.send_message(chat_id=data.chat_id, 
                                text="Ваши данные утверждены! Поздравляю!",
                                reply_markup=ikb.as_markup())

@router.callback_query(F.data == "cancell")
async def cancell_func(call: CallbackQuery):
    ikb = IKB()
    ikb.button(text="Главное меню", callback_data="main_menu")

    data = await db.time_storage.delete_timed_data(call.message.message_id)

    await call.message.answer("Данные отклонены. Уведомление продавцу отправлено!")
    await call.bot.send_message(chat_id=data.chat_id, 
                                text="Ваши данные Отклонены! Проверьте правильность данных и попробуйте снова! Данные должны соответствовать правилам /rules",
                                reply_markup=ikb.as_markup())

# Обработчик изменения данных
@router.callback_query(F.data == "no_reg_seller")
async def reg_seller_no(call: CallbackQuery):
    await no_reg_seller_menu.send_call_del(call)

@router.callback_query(F.data == "cansel_reg_seller")
async def cansel_seller_reg(call: CallbackQuery):
    await call.message.answer("Очень жаль что вы передумали...")
    await main_menu.send_call_del(call)

# endregion

# region Изменение 
# Обработчик кнопки изменения данных продавца
@router.callback_query(F.data == "redacted_seller")
async def redacted_seller_func(call: CallbackQuery):
    await editing_seller.send_call_del(call)

# Обработчик кнопки изменения названия компании
@router.callback_query(F.data == "redact_company_name")
async def edit_company_name(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название вашей компании")
    await state.set_state(EditSeller.company_name)

# Обработчик состояния изменения названия компании
@router.message(EditSeller.company_name)
async def edit_company_name(msg: Message, state: FSMContext):
    await state.update_data(company_name=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Название компании изменено")
    await state.clear()

# Обработчик кнопки изменения типа продукции
@router.callback_query(F.data == "redact_types")
async def edit_types(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите тип продукции")
    await state.set_state(EditSeller.types)

# Обработчик состояния изменения типа продукции
@router.message(EditSeller.types)
async def edit_types(msg: Message, state: FSMContext):
    await state.update_data(types=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Тип продукции изменен")
    await state.clear()

# Обработчик кнопки изменения краткого описания
@router.callback_query(F.data == "redact_short_desc")
async def edit_short_desc(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите короткое описание")
    await state.set_state(EditSeller.short_desc)

# Обработчик состояния изменения краткого описания
@router.message(EditSeller.short_desc)
async def edit_short_desc(msg: Message, state: FSMContext):
    await state.update_data(short_desc=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Краткое описание изменено")
    await state.clear()

# Обработчик кнопки изменения фотографии
#TODO {отложено} доделать возможность изменения всех фото 
@router.callback_query(F.data == "redact_photo_id")
async def edit_photo_id(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пришлите новую фотографию")
    await state.set_state(EditSeller.photo_id)

# Обработчик состояния изменения фото
@router.message(EditSeller.photo_id)
async def edit_photo_id(msg: Message, state: FSMContext):
    await state.update_data(photo_id=msg.photo[0].file_id)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Фотография изменена")
    await state.clear()

# Обработчик кнопки изменения полного описания
@router.callback_query(F.data == "redact_full_desk")
async def edit_full_desk(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите полное описание")
    await state.set_state(EditSeller.full_desc)

# Обработчик состояния изменения полного описания
@router.message(EditSeller.full_desc)
async def edit_full_desk(msg: Message, state: FSMContext):
    await state.update_data(full_desc=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    await db.seller_manager.edit_seller(state)
    await msg.answer("Полное описание изменено")
    await state.clear()

# Обработчик изменения всех данных
@router.callback_query(F.data == "full_edit_seller")
async def full_edit_seller(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название вашей компании")
    await state.set_state(RegisterSeller.company_name)
# endregion