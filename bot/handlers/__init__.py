from aiogram import Router

# Функция подключения всех роутеров из handlers
def setup_router() -> Router:
    """Подключение роутеров из handlers"""
    from . import buyer

    router = Router()
    router.include_routers(
        buyer.router,
    )

    return router
