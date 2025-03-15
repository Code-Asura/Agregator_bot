# Полные импорты
from aiogram.utils.keyboard import InlineKeyboardBuilder as Ikb
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery

from data.database import DBConnect

db = DBConnect()

class OtherMsg:
    """Класс основа для отправки сообщений"""
    def __init__(self, title_1: str,
                title_2: str | None = None,
                buttons: list[tuple[str, str]] | None = None,
                width: int = 2):
        
        self.title_1 = title_1
        self.title_2 = title_2
        self.buttons = buttons
        self.width = width

    # Генератор инлайн-клавиатуры
    def _get_markup(self):
        """Генерирует инлайн-клавиатуру"""
        ikb = Ikb()
        ikb.max_width = self.width

        for text, callback in self.buttons:
            ikb.add(InlineKeyboardButton(text=text, callback_data=callback))
        
        return ikb.as_markup()
    
    async def send_msg(self, msg: Message):
        """Отправка сообщение через Message"""
        if self.buttons is not None:

            if self.title_2 is not None:
                await msg.answer(self.title_1)
                await msg.answer(self.title_2, reply_markup=self._get_markup())

            else:
                await msg.answer(self.title_1, reply_markup=self._get_markup())

        elif self.title_2 is not None:
            await msg.answer(self.title_1)
            await msg.answer(self.title_2)
            
        else: 
            await msg.answer(self.title_1)

    async def send_call(self, call: CallbackQuery):
        """Отправка сообщений с помощью callback"""
        if self.buttons is not None:
            await call.message.answer(self.title_1, reply_markup=self._get_markup())
        else: 
            await call.message.answer(self.title_1)
        await call.answer()

    async def send_call_del(self, call: CallbackQuery):
        """Отправка сообщений с помощью callback с удалением"""
        await call.message.delete()
        if self.buttons is not None:
            await call.message.answer(self.title_1, reply_markup=self._get_markup())
        else: 
            await call.message.answer(self.title_1)
        await call.answer()

    async def send_info(self, call: CallbackQuery, types: str):
        """Отправка информационного сообщения"""
        await call.message.delete()
        sellers = await db.seller_manager.select_info(types)
        
        if not sellers:
            ikb2 = Ikb()
            ikb2.button(text="Назад ↩️", callback_data="back_food")
            await call.message.answer("В этом разделе ничего нет", reply_markup=ikb2.as_markup())
            return

        await call.message.answer(self.title_1)

        for seller in sellers: 
            ikb1 = Ikb() 
            ikb1.max_width = 2
            ikb1.button(text="Подробнее", callback_data=f"seller_{seller.id}")
            ikb1.button(text="Заказать", url=f"tg://user?id={seller.users.tg_id}")
            #ikb1.button(text="Отзывы", callback_data="reviews")
            ikb1.button(text="Назад ↩️", callback_data="back_food")
            # Отправляем сообщение с фото и описанием
            await call.message.answer_photo(
                photo=seller.photo_id,
                caption=seller.short_desc,
                reply_markup=ikb1.as_markup()
            )