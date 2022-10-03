from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.inline.menu_buttons import menu_keyboard


async def delivery_start(message: Message):
    await message.answer("Приветик)\nМеню бота:", reply_markup=menu_keyboard)


def register_delivery_start(dp: Dispatcher):
    dp.register_message_handler(delivery_start, commands=["menu", "start"], state="*")