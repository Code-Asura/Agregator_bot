# Полные импорты
from aiogram.utils.keyboard import InlineKeyboardBuilder as Ikb
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery


class OtherMsg:
    """Класс основа для отправки сообщений"""
    def __init__(self, title: str,
                buttons: list[tuple[str, str]],
                width: int = 2):
        
        self.title = title
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
        await msg.answer(self.title, reply_markup=self._get_markup())

    async def send_call(self, call: CallbackQuery):
        """Отправка сообщений с помощью callback"""
        await call.message.answer(self.title, reply_markup=self._get_markup())
        await call.answer()

    async def send_call_del(self, call: CallbackQuery):
        """Отправка сообщений с помощью callback с удалением"""
        await call.message.delete()
        await call.message.answer(self.title, reply_markup=self._get_markup())
        await call.answer()
