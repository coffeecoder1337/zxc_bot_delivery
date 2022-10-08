import json

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback
from tgbot.keyboards.inline.menu_buttons import inicialization_delivery, sets_by_restaraunt, food_by_category, \
    menu_keyboard

from tgbot.keyboards.inline.callback_datas import inicialization_delivery_callback
from tgbot.misc.states import MenuStateVkusochka


async def check_basket(call: CallbackQuery, state: FSMContext):
    with open('basket.json', 'r', encoding='utf-8') as f:
        basket = json.load(f)
        answer = ''
        for people in basket:
            out_string = f'{people}:\n'
            for item in basket[people]:
                out_string += basket[people][item][0] + " " + basket[people][item][0] + "\n"
            answer += out_string + "\n"
    if answer != '':
        await call.message.answer(answer)
    else:
        await call.message.answer("Корзина пустая")


async def make_delivery(call: CallbackQuery, state: FSMContext):
    with open('who_start_delivery.json', 'r', encoding='utf-8') as f:
        customer = json.load(f)
        if customer["is_deliver_start"]:
            if str(customer["customer"][0]) == str(call.from_user.id):
                await call.message.edit_text(
                    "Вы уже начали заказывать еду\nЗакройте заказ или добавьте блюда в общую карзину",
                    reply_markup=sets_by_restaraunt())
                await state.set_state(MenuStateVkusochka.Q1)
            else:
                await call.message.edit_text(
                    f"@{customer['customer'][1]} уже начал заказывать еду\nВы можете добавить свои блюда\nДоступные категории:",
                    reply_markup=sets_by_restaraunt())
                await state.set_state(MenuStateVkusochka.Q1)
        else:
            await call.message.edit_text("В данный момент никто не начал заказ. Вы хотите инициировать доставку?", reply_markup=inicialization_delivery)


async def dont_make_delivery_restaraunts(call: CallbackQuery):
    await call.message.edit_text("Вам придет уведомление, если кто-то начнет доставку", reply_markup=menu_keyboard)


async def make_delivery_restaraunts(call: CallbackQuery, state: FSMContext):
    with open("subscription.json", "r", encoding='utf-8') as file:
        all_subs = json.load(file)
        for sub in all_subs:
            if str(sub) == str(call.from_user.id) and all_subs[sub]:
                await call.bot.send_message(chat_id=str(sub), text="Кто-то решил заказать еду.\nУспейте добавить свое блюдо в общую карзину.")

    with open('who_start_delivery.json', 'w', encoding='utf-8') as f:
        customer = dict()
        customer["customer"] = [call.from_user.id, call.from_user.username]
        customer["is_deliver_start"] = True
        json.dump(customer, f, ensure_ascii=False)

    await call.message.edit_text("Доступные категории:", reply_markup=sets_by_restaraunt())
    await state.set_state(MenuStateVkusochka.Q1)


async def delivery_restaraunts_category(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выебите блюдо)", reply_markup=food_by_category(call.data.split(':')[1].strip()))
    await state.set_state(MenuStateVkusochka.Q2)


async def delivery_restaraunts_category_back(call: CallbackQuery, state: FSMContext):
    with open('who_start_delivery.json', 'r', encoding='utf-8') as f:
        customer = json.load(f)
        if customer["is_deliver_start"]:
            if str(customer["customer"][0]) == str(call.from_user.id):
                await call.message.edit_text(
                    "Вы уже начали заказывать еду\nЗакройте заказ или добавьте блюда в общую карзину",
                    reply_markup=sets_by_restaraunt())
                await state.set_state(MenuStateVkusochka.Q1)
            else:
                await call.message.edit_text(
                    f"@{customer['customer'][1]} уже начал заказывать еду\nВы можете добавить свои блюда\nДоступные категории:",
                    reply_markup=sets_by_restaraunt())
                await state.set_state(MenuStateVkusochka.Q1)
        else:
            await call.message.edit_text("В данный момент никто не начал заказ. Вы хотите инициировать доставку?",
                                         reply_markup=inicialization_delivery)


async def make_delivery_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
    await state.finish()


def register_make_delivery(dp: Dispatcher):
    dp.register_callback_query_handler(make_delivery, menu_callback.filter(choiсe="start_delivery"), state=None)
    dp.register_callback_query_handler(check_basket, menu_callback.filter(choiсe="basket"), state=None)
    dp.register_callback_query_handler(make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="inicialize"), state=None)
    dp.register_callback_query_handler(dont_make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="no_inicialize"), state=None)
    dp.register_callback_query_handler(make_delivery_back, menu_vkusochka_callback.filter(category="back"), state=MenuStateVkusochka.Q1)
    dp.register_callback_query_handler(delivery_restaraunts_category_back, menu_vkusochka_callback.filter(category="back"), state=MenuStateVkusochka.Q2)
    dp.register_callback_query_handler(delivery_restaraunts_category, state=MenuStateVkusochka.Q1)
