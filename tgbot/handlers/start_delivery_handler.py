import logging

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.callback_datas import menu_callback
from tgbot.keyboards.inline.menu_buttons import inicialization_delivery

from zxc_bot_delivery.tgbot.keyboards.inline.callback_datas import inicialization_delivery_callback


async def make_delivery(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("В данный момент никто не начал заказ. Вы хотите инициировать доставку?", reply_markup=inicialization_delivery)


async def make_delivery_restaraunts(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    #парсер

    await call.message.answer("Я вашу мать ебал")


def register_make_delivery(dp: Dispatcher):
    dp.register_callback_query_handler(make_delivery, menu_callback.filter(choiсe="start_delivery"), state="*")
    dp.register_callback_query_handler(make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="inicialize"), state="*")