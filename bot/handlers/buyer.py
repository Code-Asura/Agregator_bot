
# Полные импорты
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder as Rkb

# Импорт всех экземпляров для отправки сообщений
from utils.buyer_lexicon import *

# Экземпляр класса обработчика
router = Router()

# Обработчик команды /start (Главное меню)
@router.message(CommandStart())
async def start(msg: Message):
    await main_menu.send_msg(msg)

# Обработчик кнопки "Еда на заказ"
@router.callback_query(F.data == "food")
async def food(call: CallbackQuery):
    await call.message.answer("Вы перешли в раздел <b>Еда на заказ</b>")
    await food_menu.send_call(call)

# Обработчик кнопки назад в меню "Еда на заказ"
@router.callback_query(F.data == "back_main")
async def start(call: CallbackQuery):
    await call.message.answer("Вернулись в <b>Главное меню</b>")
    await main_menu.send_call(call)

# Обработчик кнопки "По типу"
@router.callback_query(F.data == "food_type")
async def food_type(call: CallbackQuery):
    await call.message.answer("Вы перешли в раздел <b>По типу</b>")
    await food_type_menu.send_call(call)

# Обработчик кнопки назад в меню "По типу"
@router.callback_query(F.data == "back_food")
async def bach_food(call: CallbackQuery):
    await call.message.answer("Вы вернулись в меню <b>Еда на заказ</b>")
    await food_menu.send_call(call)

# Обработчик кнопки "По кухне"
@router.callback_query(F.data == "kitchen")
async def food_type(call: CallbackQuery):
    await call.message.answer("Вы перешли к выбору <b>По кухне</b>")
    await to_kitchen_menu.send_call(call)

# Обработчик кнопки "По назначению"
@router.callback_query(F.data == "appointment")
async def food_type(call: CallbackQuery):
    await call.message.answer("Вы перешли к выбору <b>По назначению</b>")
    await appointment_menu.send_call(call)

# Обработчик кнопки "Готовая еда"
@router.callback_query(F.data == "ready_made_food")
async def food_type(call: CallbackQuery):
    await call.message.answer("Вы перешли к выбору <b>Готовой еды</b>")
    await ready_made_food_menu.send_call(call)

# Обработчик заглушек
@router.callback_query(F.data == "plug")
async def food_type(call: CallbackQuery):
    await call.message.answer("Бот работает в тестовом режиме.\n"
                              "Данный раздел скоро запустится.\n"
                              "Активный раздел - Еда на заказ"")")
    
# Обработчик кнопки "Отзывы"
@router.callback_query(F.data == "reviews")
async def food_type(call: CallbackQuery):
    await call.message.answer("Пока этот раздел не нужен")

# Обработчик кнопки "Обратная связь"
@router.callback_query(F.data == "feedback")
async def food_type(call: CallbackQuery):
    await call.message.answer("😊Мы всегда рады вашим отзывам и любой обратной связи!\n"
                              "📩Если у вас есть предложения, замечания или простослова поддержки.\n"
                              "Если вы нашли ошибку, приложите, пожалуйста, скриншот или подробное описание.\n"
                              "Мы внимательно читаем каждое сообщение и стремимся сделать наш сервис еще лучше.")