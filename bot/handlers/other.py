
# Полные импорты
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

# Экземпляр класса обработчика
router = Router()

# Обработчик команды /start (Главное меню)
@router.message(CommandStart())
async def start(msg: Message):
    from utils import main_menu
    await main_menu.send_msg(msg)

# Обработчик кнопки назад в меню "Еда на заказ"
@router.callback_query(F.data == "back_main")
async def start(call: CallbackQuery):
    from utils import main_menu
    await main_menu.send_call(call)

# Обработчик кнопки "Еда на заказ"
@router.callback_query(F.data == "food")
async def food(call: CallbackQuery):
    from utils import food_menu
    await food_menu.send_call(call)

@router.callback_query(F.data == "back_food")
async def bach_food(call: CallbackQuery):
    await call.message.answer("Вы вернулись в меню Еда на заказ")
    await food(call) 


# Обработчик кнопки "По типу"
@router.callback_query(F.data == "food_type")
async def food_type(call: CallbackQuery):
    from utils import food_type_menu
    await food_type_menu.send_call(call)

# Обработчик кнопки "По кухне"
@router.callback_query(F.data == "kitchen")
async def food_type(call: CallbackQuery):
    from utils import to_kitchen_menu
    await to_kitchen_menu.send_call(call)

# Обработчик кнопки "По назначению"
@router.callback_query(F.data == "appointment")
async def food_type(call: CallbackQuery):
    from utils import appointment_menu
    await appointment_menu.send_call(call)

# Обработчик кнопки "Готовая еда"
@router.callback_query(F.data == "ready_made_food")
async def food_type(call: CallbackQuery):
    from utils import ready_made_food_menu
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