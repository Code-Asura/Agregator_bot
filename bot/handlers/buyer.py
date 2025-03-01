
# Полные импорты
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

# Импорт класса работы с базой данных
from data.database import DBConnect

# Импорт всех экземпляров для отправки сообщений
from utils.buyer_lexicon import *

# Экземпляр класса обработчика
router = Router()
# Экземпляр класса БД
db = DBConnect()

# Обработчик команды /start (Главное меню)
@router.message(CommandStart())
async def start(msg: Message):
    await msg.delete()
    await db.user_manager.add_user(
        tg_id=msg.from_user.id,
        username=msg.from_user.username,
        name=msg.from_user.first_name
    )
    await start_message.send_msg(msg)


@router.callback_query(F.data == "next_start_msg")
async def next_start_msg_func(call: CallbackQuery):
    await next_start_msg.send_call(call)

@router.callback_query(F.data == "main_menu")
async def main_menu_func(call: CallbackQuery):
    await main_menu.send_call(call)

# Обработчик кнопки "Еда на заказ"
@router.callback_query(F.data == "food")
async def food(call: CallbackQuery):
    await call.message.answer("Вы перешли в раздел <b>Еда на заказ</b>")
    await food_type_menu.send_call_del(call)

# # Обработчик кнопки назад в меню "Еда на заказ"
# @router.callback_query(F.data == "back_main")
# async def start(call: CallbackQuery):
#     await call.message.answer("Вернулись в <b>Главное меню</b>")
#     await main_menu.send_call_del(call)

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

# Обработчик заглушек
@router.callback_query(F.data == "plug")
async def food_type(call: CallbackQuery):
    await call.message.answer("Бот работает в тестовом режиме.\n"
                              "Данный раздел скоро запустится.\n"
                              "Активный раздел - Еда на заказ"")")
    
# Обработчик кнопки "Отзывы"
# @router.callback_query(F.data == "reviews")
# async def food_type(call: CallbackQuery):
#     await call.message.answer("Пока этот раздел не нужен")

# Обработчик кнопки "Обратная связь"
@router.callback_query(F.data == "feedback")
async def feedback_call(call: CallbackQuery):
    await call.message.answer("😊Мы всегда рады вашим отзывам и любой обратной связи!\n"
                              "📩Если у вас есть предложения, замечания или простослова поддержки.\n"
                              "Если вы нашли ошибку, приложите, пожалуйста, скриншот или подробное описание.\n"
                              "Мы внимательно читаем каждое сообщение и стремимся сделать наш сервис еще лучше.")
    
@router.message(Command('feedback'))
async def feedback_cmd(msg: Message):
    pass