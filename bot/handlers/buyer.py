
# Полные импорты
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder as IKB

from data.configs import Feedback
from data import config

# Импорт класса работы с базой данных
from data.database import DBConnect

# Импорт всех экземпляров для отправки сообщений
from utils.buyer_lexicon import *

# Экземпляр класса обработчика
router = Router()
# Экземпляр класса БД
db = DBConnect()

# Обработчик команды /start
@router.message(CommandStart())
async def start(msg: Message):
    await msg.delete()
    await db.user_manager.add_user(
        tg_id=msg.from_user.id,
        username=msg.from_user.username,
        name=msg.from_user.first_name
    )
    await start_message.send_msg(msg)

# Обработчик для показа следующего приветственного сообщения
@router.callback_query(F.data == "next_start_msg")
async def next_start_msg_func(call: CallbackQuery):
    await next_start_msg.send_call(call)

# Обработчик показа главного меню
@router.callback_query(F.data == "main_menu")
async def main_menu_func(call: CallbackQuery):
    await main_menu.send_call(call)

# Обработчик кнопки "Еда на заказ"
@router.callback_query(F.data == "food")
async def food(call: CallbackQuery):
    await call.message.answer("Вы перешли в раздел <b>Еда на заказ</b>")
    await food_type_menu.send_call_del(call)

# Обработчик кнопки назад в меню "Еда на заказ"
@router.callback_query(F.data == "back_main")
async def start(call: CallbackQuery):
    await call.message.answer("Вернулись в <b>Главное меню</b>")
    await main_menu.send_call_del(call)

# region Пока не нужное
# # Обработчик кнопки "По типу"
# @router.callback_query(F.data == "food_type")
# async def food_type(call: CallbackQuery):
#     await call.message.answer("Вы перешли в раздел <b>По типу</b>")
#     await food_type_menu.send_call_del(call)

# # Обработчик кнопки назад в меню "По типу"
# @router.callback_query(F.data == "back_food")
# async def bach_food(call: CallbackQuery):
#     await call.message.answer("Вы вернулись в меню <b>Еда на заказ</b>")
#     await food_menu.send_call_del(call)

# # Обработчик кнопки "По кухне"
# @router.callback_query(F.data == "kitchen")
# async def food_type(call: CallbackQuery):
#     await call.message.answer("Вы перешли к выбору <b>По кухне</b>")
#     await to_kitchen_menu.send_call_del(call)

# # Обработчик кнопки "По назначению"
# @router.callback_query(F.data == "appointment")
# async def food_type(call: CallbackQuery):
#     await call.message.answer("Вы перешли к выбору <b>По назначению</b>")
#     await appointment_menu.send_call_del(call)

# # Обработчик кнопки "Готовая еда"
# @router.callback_query(F.data == "ready_made_food")
# async def food_type(call: CallbackQuery):
#     await call.message.answer("Вы перешли к выбору <b>Готовой еды</b>")
#     await ready_made_food_menu.send_call_del(call)
    
# Обработчик кнопки "Отзывы"
# @router.callback_query(F.data == "reviews")
# async def food_type(call: CallbackQuery):
#     await call.message.answer("Пока этот раздел не нужен")
# endregion

# Обработчик заглушек
@router.callback_query(F.data == "plug")
async def food_type(call: CallbackQuery):
    await call.message.answer("Бот работает в тестовом режиме.\n"
                              "Данный раздел скоро запустится.\n"
                              "Активный раздел - Еда на заказ")

# region Обратная связь
# Обработчик команды обратная связь
@router.callback_query(F.data == "feedback")
async def feedback_call_func(call: CallbackQuery, state: FSMContext):
    await feedback_call.send_call_del(call)
    await call.message.answer("Отправьте ваше обращение (текст)")
    await state.set_state(Feedback.message)

# Обработчик кнопки обратная связь
@router.message(Command('feedback'))
async def feedback_cmd(msg: Message, state: FSMContext):
    await feedback_msg.send_msg(msg)
    await msg.answer("Отправьте ваше обращение (текст)")
    await state.set_state(Feedback.message)

# Обработчик состояния текста сообщения
@router.message(Feedback.message)
async def feedback_photo_func(msg: Message, state: FSMContext):
    await state.update_data(message=msg.text)
    await feedback_photo.send_msg(msg)
    await state.set_state(Feedback.photo)

# Обработчик состояния фото если есть
#TODO Добавить возможность получать альбом
@router.message(Feedback.photo)
async def feedback_func(msg: Message, state: FSMContext):
    await state.update_data(photo=msg.photo[0].file_id)
    data = await state.get_data()
    await msg.answer_photo(
        photo=data['photo'],
        caption=data['message']
    )
    await feedback_y_n.send_msg(msg)

# Обработчик кнопки "пропустить" фото
@router.callback_query(F.data == "skip_feedback_photo")
async def feedback_phot_skipped(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.answer(str(data['message']))
    await feedback_y_n.send_call(call)

# Обработчик кнопки подтверждения отправки
@router.callback_query(F.data == "yes_send_feedback")
async def yes_feedback_send(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    ikb = IKB()
    ikb.button(text=f"{call.from_user.first_name}",
               url=f"tg://user?id={call.from_user.id}")

    print(config.feedback_grup)

    try:
        await call.bot.send_photo(
            chat_id=config.feedback_grup,
            photo=data['photo'],
            caption=data['message'],
            reply_markup=ikb.as_markup()
        )
        await call.message.answer("Отправлено ☺️")
        state.clear()
    except:
        await call.bot.send_message(
            chat_id=config.feedback_grup,
            text=data['message'],
            reply_markup=ikb.as_markup()
        )
        await call.message.answer("Отправлено ☺️")
        state.clear()

#TODO Добавить обработку отказа и изменения
# endregion