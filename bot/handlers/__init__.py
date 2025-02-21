from aiogram import Router

# Функция подключения всех роутеров из handlers
def setup_router() -> Router:
    """Подключение роутеров из handlers"""
    from . import buyer
<<<<<<< HEAD
=======
    from . import seller
>>>>>>> 780a06e (добавлена регистрация продавца и проверка)

    router = Router()
    router.include_routers(
        buyer.router,
<<<<<<< HEAD
=======
        seller.router
>>>>>>> 780a06e (добавлена регистрация продавца и проверка)
    )

    return router
