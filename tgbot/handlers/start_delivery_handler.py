import logging

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.callback_datas import menu_callback
from tgbot.keyboards.inline.menu_buttons import inicialization_delivery

from tgbot.keyboards.inline.callback_datas import inicialization_delivery_callback

import os, re, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test_parser import VkusnoITochka_parser


async def make_delivery(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("В данный момент никто не начал заказ. Вы хотите инициировать доставку?", reply_markup=inicialization_delivery)


async def make_delivery_restaraunts(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("Загружаю рестораны....")
    #парсер
    VkusnoITochka_parser().get_menu()
    await call.message.answer("Все отлично!")


def register_make_delivery(dp: Dispatcher):
    dp.register_callback_query_handler(make_delivery, menu_callback.filter(choiсe="start_delivery"), state="*")
    dp.register_callback_query_handler(make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="inicialize"), state="*")