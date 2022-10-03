import logging

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.callback_datas import menu_callback
from tgbot.keyboards.inline.menu_buttons import inicialization_delivery


async def make_delivery(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("В данный момент никто не начал заказ. Вы хотите инициировать доставку?", reply_markup=inicialization_delivery)


def register_make_delivery(dp: Dispatcher):
    dp.register_callback_query_handler(make_delivery, menu_callback.filter(choiсe="start_delivery"), state="*")