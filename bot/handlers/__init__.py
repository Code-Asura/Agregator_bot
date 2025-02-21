from aiogram import Router

# Функция подключения всех роутеров из handlers
def setup_router() -> Router:
    """Подключение роутеров из handlers"""
    from . import buyer
    from . import seller

    router = Router()
    router.include_routers(
        buyer.router,
        seller.router
    )

    return router
