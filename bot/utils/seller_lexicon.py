from . import OtherMsg

seller_reg_menu = OtherMsg(
    title = "Все данные указаны правильно?",
    buttons = [
        ("Да", "yes_reg_seller"),
        ("Нет", "no_reg_seller"),
    ]
)

seller_true = OtherMsg(
    title="Вы уже зарегестрированы как продавец",
    buttons=[
        ("Редактировать", "redacted_seller")
    ]
)

no_reg_seller_menu = OtherMsg(
    title="Что вы хотите изменить?",
    buttons=[
        ("Название", "redact_company_name"),
        ("Тип продукта", "redact_types"),
        ("Фото", "redact_photo_id"),
        ("Короткое описание", "redact_short_desc"),
        ("Полное описание", "redact_full_desk"),
        ("Всё", "full_edit_seller")
    ]
)

redacted_seller = OtherMsg(
    title="Что вы хотите изменить?",
    buttons=[
        ("Название", "edit_company_name"),
        ("Тип продукта", "edit_types"),
        ("Фото", "edit_photo_id"),
        ("Короткое описание", "edit_short_desc"),
        ("Полное описание", "edit_full_desk"),
        ("Всё", "full_edit_seller")
    ]
)
