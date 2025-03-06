from . import OtherMsg


start_message = OtherMsg(
    title="✨ Добро пожаловать в УслугиARBA! ✨\n\n"

          "🛠Бот работает в тестовом режиме 🛠\n\n"

          "Мы совсем недавно запустили бот и сейчас проверяем его работу.\n"
          "Если Вы заметили ошибки или есть идеи его по улучшению - пишите через\n"
          'форму "Обратной связи" в главном меню бота!\n\n'

          "Сейчас работает категория - Еда на заказ!\n"
          "Мы собираем регистрации продавцов по остальным категориям и в ближайшее время откроем их для всех!"

          "✅Подпишись на канал с новостями и обновлениями https://t.me/+LVWu_IMny0o3ZDQ6"
          '✨ Добро пожаловать в "УслугиARBA"! ✨\n\n',
          buttons=[
              ("Продолжить", "next_start_msg")
          ]
)

next_start_msg = OtherMsg(
    title="🎯 В этом боте собраны специалисты Аргентины!\n\n"

          "Что можно найти:\n"
          "🍕 Доставка еды\n"
          "🌐 Переводчики\n"
          "❄️ Ремонт кондиционеров\n"
          "💰 Обмен валюты\n"
          "🚗 Трансфер\n"
          "⚖️ Юридические услуги\n"
          "💪 Фитнес-тренеры\n"
          "💅 Маникюр\n"
          "✂️ Парикмахеры\n"
          "🌍 Экскурсии\n"
          "...и многое другое!\n\n"

          "👇 Начните поиск нужной услуги через меню ниже\n"
          "📢 Расскажите друзьям и специалистам о боте\n"
          "✅Подпишись на канал с новостями и обновлениями https://t.me/+LVWu_IMny0o3ZDQ6\n\n"

          "Если вы специалист:\n"
          "✅ Нажмите Меню (слева от клавиатуры)\n"
          "📝 Заполните форму регистрации\n\n"

          "P.S. Поделитесь своим мнением через обратную связь 💬",
          buttons=[
              ("Главное меню", "main_menu")
          ]
)


# Главное меню
main_menu = OtherMsg(
    title = "Вы в <b>Главном меню</b>",
    buttons = [
        ("🍕Еда🍱", "food"),
        ("⚡️Услуги💼", "plug"), #services
        ("🏠Недвижимость🏢", "plug"), #estate
        ("🍷Русские заведения🎵", "plug"), #russian_est
        ("💰Обменники🔄", "plug"), #exchangers
        #("Товары", "plug"), #products
        ("🎉Мероприятия📅", "plug"), #events
        #("Отзывы", "reviews"),
        ("💬Обратная связь📝", "feedback")
    ]
)

# Меню "Еда на заказ"
# food_menu = OtherMsg(
#     title = "Выберите категорию",
#     buttons = [
#         ("По типу", "food_type"),
#         ("По Кухне", "kitchen"),
#         ("По назначению", "appointment"),
#         ("Меню на неделю", "for_week"),
#         ("По отзывам", "to_reviews"),
#         ("Назад", "back_main")
#     ]
# )

# Меню кнопки "По типу"
food_type_menu = OtherMsg(
    title = "Выберите категорию",
    buttons = [
        ("Готовая еда 🍱", "ready_made_food"),
        ("Мясные изделия 🥩", "meat_products"),
        ("Полуфабрикаты 🥟", "semi_finished"),
        ("Десерты и выпечка 🍰", "desserts_pastries"),
        ("Диетическая еда 🥗", "diet_food"),
        ("Консервация и соусы 🥫", "konc_sous_food"),
        ("Напитки 🥤", "drinks"),
        ("Назад ↩️", "back_food")
    ]
)

# Меню кнопки "По кухне"
to_kitchen_menu = OtherMsg(
    title = "Выберите кухню",
    buttons = [
        ("Русская", "russian"),
        ("Аргентинская", "argentina"),
        ("Итальянская", "italian"),
        ("Грузинская", "georgian"),
        ("Японская", "japanes"),
        ("Другое", "more"),
        ("Назад ↩️", "back_food")
    ]
)

# Меню кнопки "По назначению"
appointment_menu = OtherMsg(
    title = "Выберите назначение",
    width = 1,
    buttons = [
        ("На каждый день", "every_day"),
        ("На праздник", "holiday"),
        ("Для детей", "children"),
        ("Для мероприятий", "for_events"),
        ("Назад ↩️", "food")
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
        ("Назад ↩️", "food_type")
    ]
)

feedback_msg = OtherMsg(
    title="💬 Пожалуйста, опишите свою проблему подробно.\n"
          "Если есть скриншоты, обязательно приложите их - это поможет быстрее решить вопрос! 📸\n\n"

          "Мы внимательно изучим ваше сообщение и ответим в ближайшее время. ⏳\n\n"

          "Благодарим за понимание! ❤️",
          buttons=[
              ("Назад ↩️", "back_main")
          ]
)

feedback_call = OtherMsg(
    title="😊Мы всегда рады вашим отзывам и любой обратной связи!\n"
          "📩Если у вас есть предложения, замечания или простослова поддержки.\n"
          "Если вы нашли ошибку, приложите, пожалуйста, скриншот или подробное описание.\n"
          "Мы внимательно читаем каждое сообщение и стремимся сделать наш сервис еще лучше.",
    buttons=[
              ("Назад ↩️", "back_main")
          ]
)

feedback_photo = OtherMsg(
    title="Сохранил, теперь отправьте фото",
    buttons=[
        ("Пропустить", "skip_feedback_photo")
    ]
)

feedback_y_n = OtherMsg(
    title="Подтвердите отправку",
    buttons=[
        ("Изменить", "edit_feedback"),
        ("Не отправлять", "no_send_feedback"),
        ("Отправить 📨", "yes_send_feedback")
    ]
)