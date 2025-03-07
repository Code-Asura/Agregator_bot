from . import OtherMsg

seller_start_reg = OtherMsg(
    title_1 = "Вы перешли в раздел <b>Регистрация продавца</b>",
    title_2 = "Введите название вашей компании"
)

seller_reg_menu = OtherMsg(
    title_1 = "Все данные указаны правильно?",
    buttons = [
        ("Да", "yes_reg_seller"),
        ("Нет", "no_reg_seller"),
        ("Отменить", "cansel_reg_seller")
    ]
)

seller_true = OtherMsg(
    title_1 = "Вы уже зарегестрированы как продавец",
    buttons = [
        ("Редактировать", "redacted_seller")
    ]
)

no_reg_seller_menu = OtherMsg(
    title_1 = "Что вы хотите изменить?",
    buttons = [
        ("Название", "redact_company_name"),
        ("Тип продукта", "redact_types"),
        ("Фото", "redact_photo_id"),
        ("Короткое описание", "redact_short_desc"),
        ("Полное описание", "redact_full_desk"),
        ("Всё", "full_edit_seller")
    ]
)

editing_seller = OtherMsg(
    title_1 = "Что вы хотите изменить?",
    buttons=[
        ("Название", "edit_company_name"),
        ("Тип продукта", "edit_types"),
        ("Фото", "edit_photo_id"),
        ("Короткое описание", "edit_short_desc"),
        ("Полное описание", "edit_full_desk"),
        ("Всё", "full_edit_seller")
    ]
)

reg_seller_types_menu = OtherMsg(
    title_1 = "Выберите тип продукции",
    buttons = [
        ("🍕Еда🍱", "food_reg_seller"),
        ("⚡️Услуги💼", "plug"), #services
        ("🏠Недвижимость🏢", "plug"), #estate
        ("🍷Русские заведения🎵", "plug"), #russian_est
        ("💰Обменники🔄", "plug"), #exchangers
        #("Товары", "plug"), #products
        ("🎉Мероприятия📅", "plug"), #events
        #("Отзывы", "reviews"),
    ]
)

reg_seller_food_type_menu = OtherMsg(
    title_1 = "Выберите категорию",
    buttons = [
        ("Готовая еда 🍱", "reg_seller_ready_made_food"),
        ("Мясные изделия 🥩", "reg_seller_meat_products"),
        ("Полуфабрикаты 🥟", "reg_seller_semi_finished"),
        ("Десерты и выпечка 🍰", "reg_seller_desserts_pastries"),
        ("Диетическая еда 🥗", "reg_seller_diet_food"),
        ("Консервация и соусы 🥫", "reg_seller_konc_sous_food"),
        ("Напитки 🥤", "reg_seller_drinks"),
        ("Назад ↩️", "reg_seller_back_food")
    ]
)
