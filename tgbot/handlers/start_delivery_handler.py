import logging

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback
from tgbot.keyboards.inline.menu_buttons import inicialization_delivery, sets_by_restaraunt, food_by_category, \
    sets_by_restaraunt_back, menu_keyboard

from tgbot.keyboards.inline.callback_datas import inicialization_delivery_callback
from tgbot.misc.states import MenuStateVkusochka


async def make_delivery(call: CallbackQuery):
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("В данный момент никто не начал заказ. Вы хотите инициировать доставку?", reply_markup=inicialization_delivery)


async def dont_make_delivery_restaraunts(call: CallbackQuery):
    await call.message.answer("Вам придет уведомление, если кто-то начнет доставку", reply_markup=menu_keyboard)


async def make_delivery_restaraunts(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Загружаю категории....")
    await call.message.answer("Доступные категории:", reply_markup=sets_by_restaraunt())
    await state.set_state(MenuStateVkusochka.Q1)


async def delivery_restaraunts_category(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выебите блюдо)", reply_markup=food_by_category(call.data.split(':')[1].strip()))
    await state.set_state(MenuStateVkusochka.Q2)


async def delivery_restaraunts_category_back(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Доступные категории:", reply_markup=sets_by_restaraunt_back())
    await state.set_state(MenuStateVkusochka.Q1)


async def make_delivery_back(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Вы вышли из заказа доставки. Хотите инициировать доставку?", reply_markup=inicialization_delivery)
    await state.finish()


def register_make_delivery(dp: Dispatcher):
    dp.register_callback_query_handler(make_delivery, menu_callback.filter(choiсe="start_delivery"), state=None)
    dp.register_callback_query_handler(make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="inicialize"), state=None)
    dp.register_callback_query_handler(dont_make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="no_inicialize"), state=None)
    dp.register_callback_query_handler(make_delivery_back, menu_vkusochka_callback.filter(category="back"), state=MenuStateVkusochka.Q1)
    dp.register_callback_query_handler(delivery_restaraunts_category_back, menu_vkusochka_callback.filter(category="back"), state=MenuStateVkusochka.Q2)
    dp.register_callback_query_handler(delivery_restaraunts_category, state=MenuStateVkusochka.Q1)
