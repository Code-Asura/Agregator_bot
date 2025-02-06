from . import OtherMsg

# Главное меню
main_menu = OtherMsg(
    title = "Добро пожаловать в\n<b>Главное меню</b>",
    buttons = [
        ("Еда на заказ", "food"),
        ("Услуги", "plug"), #services
        ("Недвижимость", "plug"), #estate
        ("Русские заведения", "plug"), #russian_est
        ("Обменники", "plug"), #exchangers
        #("Товары", "plug"), #products
        ("Мероприятия", "plug"), #events
        #("Отзывы", "reviews"),
        ("Обратная связь", "feedback")
    ]
)

# Меню "Еда на заказ"
food_menu = OtherMsg(
    title = "Добро пожаловать в\n<b>Еда на заказ</b>",
    buttons = [
        ("По типу", "food_type"),
        ("По Кухне", "kitchen"),
        ("По назначению", "appointment"),
        ("Меню на неделю", "for_week"),
        ("По отзывам", "to_reviews"),
        ("Назад", "back_main")
    ]
)

# Меню кнопки "По типу"
food_type_menu = OtherMsg(
    title = "Добро пожаловать в\n<b>По типу еды</b>",
    buttons = [
        ("Готовая еда", "ready_made_food"),
        ("Мясные изделия", "meat_products"),
        ("Полуфабрикаты", "semi_finished"),
        ("Десерты и выпечка", "desserts_pastries"),
        ("Диетическая еда", "diet_food"),
        ("Концервация и соусы", "diet_food"),
        ("Напитки", "drinks"),
        ("Назад", "back_food")
    ]
)

# Меню кнопки "По кухне"
to_kitchen_menu = OtherMsg(
    title = "Добро пожаловать в\n<b>По кухне</b>",
    buttons = [
        ("Русская", "russian"),
        ("Аргентинская", "argentina"),
        ("Итальянская", "italian"),
        ("Грузинская", "georgian"),
        ("Японская", "japanes"),
        ("Другое", "more"),
        ("Назад", "food")
    ]
)

# Меню кнопки "По назначению"
appointment_menu = OtherMsg(
    title = "Добро пожаловать в\n<b>По назначению</b>",
    width = 1,
    buttons = [
        ("На каждый день", "every_day"),
        ("На праздник", "holiday"),
        ("Для детей", "children"),
        ("Для мероприятий", "for_events"),
        ("Назад", "food")
    ]
)

# Меню кнопки "Готовая еда"
ready_made_food_menu = OtherMsg(
    title = "Нажмите для просмотра меню\n"
            "1. Машкина каша  - описание + основное фото + балл отзывов\n"
            "2. Лада-седан БАКЛАЖАНовые рулетики - описание + основное фото + балл отзывов\n"
            "3. Русская кухня на заказ - описание + основное фото + балл отзывов\n"
            "4. Есть хотите? - описание + основное фото + балл отзывов\n"
            "5. ИП Арутюнян - описание + основное фото + балл отзывов",
    buttons = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("Ещё", "more"),
        ("Назад", "food_type")
    ]
)
