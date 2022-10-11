import json
import re

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback, basket_callback, \
    restauranta_callback
from tgbot.keyboards.inline.menu_buttons import inicialization_delivery, sets_by_restaraunt, food_by_category, \
    menu_keyboard, basket_back, edit_basket_keyboard, choose_restaraunt_keyboard

from tgbot.keyboards.inline.callback_datas import inicialization_delivery_callback
from tgbot.misc.states import MenuStateVkusochka, Basket


def find_page(category, file):
    with open(f"{file}.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
    out = 0
    for ct in vkusochka_menu:
        if str(vkusochka_menu[ct][0]) == str(category):
            out = ct
    return len(vkusochka_menu[out][1:])


async def client_basket_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state(Basket.W2)
    await call.message.edit_text("Выберите блюдо, которое хотите удалить", reply_markup=edit_basket_keyboard(call.from_user.username))


async def choose_restaraunt(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите ресторан", reply_markup=choose_restaraunt_keyboard())
    await state.set_state(MenuStateVkusochka.Q4)


async def choose_restaraunt_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
    await state.finish()


async def delete_from_basket(call: CallbackQuery, state: FSMContext):
    data = call.data
    data1 = str(data).split(":")[1]
    food = str(data1).split("/")[0]
    restaurant = str(data1).split("/")[1]
    with open("basket.json", "r", encoding='utf-8') as file:
        basket = json.load(file)
    food_deleted = "Ничего не"
    trigger = 0
    for rest in basket[call.from_user.username]:
        for item in basket[call.from_user.username][rest]:
            print(str(basket[call.from_user.username][str(restaurant)]), int(food))
            if str(item) == str(basket[call.from_user.username][str(restaurant)][int(food)]):
                food_deleted = item[0]
                basket[call.from_user.username][rest].remove(item)
                trigger = 1
                break
        if basket[call.from_user.username][rest] == list():
            basket[call.from_user.username].pop(rest)
            break
        if trigger == 1:
            break
    with open("basket.json", "w", encoding='utf-8') as file:
        if call.from_user.username in basket.keys():
            if basket[call.from_user.username] == dict():
                basket.pop(call.from_user.username)
                if basket.keys() == list():
                    basket = dict()
                file.write(json.dumps(basket, ensure_ascii=False))
                await call.answer(text=f"{food_deleted} было удалено из вашей корзины\nВаша корзина пустая\nВы возвращены в меню", show_alert=True)
                await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
                await state.finish()
                return
            file.write(json.dumps(basket, ensure_ascii=False))
            file.close()
            await call.answer(text=f"{food_deleted} было удалено из вашей корзины", show_alert=True)
            await call.message.edit_text("Выберите блюдо, которое хотите удалить", reply_markup=edit_basket_keyboard(call.from_user.username))
        else:
            await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
            await state.finish()


async def client_basket_clear(call: CallbackQuery, state: FSMContext):
    with open('basket.json', 'r', encoding='utf-8') as file:
        basket = json.load(file)
        for client in basket:
            if str(client) == str(call.from_user.username):
                basket.pop(client)
                break
    with open('basket.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(basket, ensure_ascii=False))
    await call.answer(text="Ваша корзина была очищена!", show_alert=True)
    await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
    await state.finish()


async def check_basket(call: CallbackQuery, state: FSMContext):
    with open('basket.json', 'r', encoding='utf-8') as f:
        basket = json.load(f)
    answer = ''
    result = 0
    for people in basket:
        out_string = f'@{people}:\n'
        summary = 0
        for restaurant in basket[people].keys():
            out_string += "\nРесторан " + str(restaurant) + ": \n"
            for item in basket[people][restaurant]:
                summary += int(item[1][0])
                out_string += str(item[0]) + " " + str(item[1][0]) + "\n"
        answer += out_string + "============\n" + f"Итог: {summary} руб" + "\n\n"
        result += summary
    answer += "------------\n" + f"Всего: {result} руб"
    if answer != '':
        await call.message.edit_text(answer, reply_markup=basket_back(call.from_user.id, call.from_user.username))
        await state.set_state(Basket.W1)


async def delivery_end(call: CallbackQuery, state: FSMContext):
    with open('clients_summ_spend.json', 'r', encoding='utf-8') as file:
        history = json.load(file)
    with open('basket.json', 'r', encoding='utf-8') as file:
        basket = json.load(file)
    for people in basket:
        sum = 0
        for rest in basket[people]:
            for item in basket[people][rest]:
                sum += int(item[1][0])
        if people not in history.keys():
            history[people] = sum
        history[people] = int(history[people]) + sum
    with open('clients_summ_spend.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(history, ensure_ascii=False))
    with open('who_start_delivery.json', 'r', encoding='utf-8') as file:
        deliver = json.load(file)
        deliver['customer'] = [000000000, ""]
        deliver['is_deliver_start'] = False
    with open('who_start_delivery.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(deliver, ensure_ascii=False))
    with open('basket.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(dict(), ensure_ascii=False))
    await call.answer(text="Корзина очищена!", show_alert=True)
    await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
    with open('subscription.json', 'r', encoding='utf-8') as file:
        subscribers = json.load(file)
        for subscriber in subscribers:
            if subscribers[subscriber] and str(subscriber) != str(call.from_user.id):
                await call.bot.send_message(chat_id=str(subscriber), text=f"@{call.from_user.username} заказал еду, корзина закрыта.")
    await state.finish()


async def make_delivery(call: CallbackQuery, state: FSMContext):
    try:
        restaurant_id = str(call.data).split(':')[1]                                    #задание даты
        with open('restaurants.json', 'r', encoding='utf-8') as file:
            restaurants = json.load(file)
        file = restaurants['restaurants'][int(restaurant_id)]
        await state.update_data(file=file)
    except:
        pass
    with open(f'who_start_delivery.json', 'r', encoding='utf-8') as f:
        customer = json.load(f)
        if customer["is_deliver_start"]:
            if str(customer["customer"][0]) == str(call.from_user.id):
                await call.message.edit_text(
                    "Вы уже начали заказывать еду\nЗакройте заказ или добавьте блюда в общую карзину\nДоступные рестораны:",
                    reply_markup=choose_restaraunt_keyboard())
                await state.set_state(MenuStateVkusochka.Q4)
            else:
                await call.message.edit_text(
                    f"@{customer['customer'][1]} уже начал заказывать еду\nВы можете добавить свои блюда\nДоступные рестораны:",
                    reply_markup=choose_restaraunt_keyboard())
                await state.set_state(MenuStateVkusochka.Q4)
        else:
            await call.message.edit_text("В данный момент никто не начал заказ. Вы хотите инициировать доставку?", reply_markup=inicialization_delivery)
            await state.set_state(MenuStateVkusochka.Q3)


async def choose_category(call: CallbackQuery, state: FSMContext):
    restaurant_id = str(call.data).split(':')[1]  # задание даты
    with open('restaurants.json', 'r', encoding='utf-8') as file:
        restaurants = json.load(file)
    file = restaurants['restaurants'][int(restaurant_id)]
    await state.update_data(file=file)
    await call.message.edit_text("Загружаю категории...\nПридется подождать, этот процесс необходим раз в сутки")
    await call.message.edit_text("Выбирай категорию нахуй", reply_markup=sets_by_restaraunt(file))
    await state.set_state(MenuStateVkusochka.Q1)


async def dont_make_delivery_restaraunts(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вам придет уведомление, если кто-то начнет доставку", reply_markup=menu_keyboard)
    await state.finish()


async def make_delivery_restaraunts(call: CallbackQuery, state: FSMContext):
    with open("subscription.json", "r", encoding='utf-8') as file:
        all_subs = json.load(file)
        for sub in all_subs:
            if str(sub) != str(call.from_user.id) and all_subs[sub]:
                await call.bot.send_message(chat_id=str(sub), text="Кто-то решил заказать еду.\nУспейте добавить свое блюдо в общую карзину.")
            elif str(sub) == str(call.from_user.id):
                await call.answer(text="Вы инициировали доставку!", show_alert=True)
    with open('who_start_delivery.json', 'w', encoding='utf-8') as f:
        customer = dict()
        customer["customer"] = [call.from_user.id, call.from_user.username]
        customer["is_deliver_start"] = True
        json.dump(customer, f, ensure_ascii=False)
    await call.message.edit_text(
        "Загружаю доступные рестораны...",
        reply_markup=None)
    await call.message.edit_text("Выберите ресторан", reply_markup=choose_restaraunt_keyboard())
    await state.set_state(MenuStateVkusochka.Q4)


async def delivery_restaraunts_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file = data.get('file')
    lenth = find_page(call.data.split(':')[1].strip(), file)
    await call.message.edit_text(f"Выебите блюдо)\nСтраница: {1}/{lenth}", reply_markup=food_by_category(call.data.split(':')[1].strip(), 0, file))
    await state.update_data(page=0)
    await state.update_data(category=call.data.split(':')[1].strip())
    await state.set_state(MenuStateVkusochka.Q2)


async def delivery_restaraunts_category_left(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = int(data.get('page'))
    category = data.get('category')
    file = data.get('file')
    lenth = find_page(category, file)
    if page - 1 >= 0:
        page -= 1
    else:
        page = lenth - 1
    await state.update_data(page=page)
    await call.message.edit_text(f"Выебите блюдо)\nСтраница: {page+1}/{lenth}", reply_markup=food_by_category(data=category, page=page, file=file))


async def delivery_restaraunts_category_right(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')
    category = data.get('category')
    file = data.get('file')
    lenth = find_page(category, file)
    if page + 1 == lenth:
        page = 0
    else:
        page += 1
    await state.update_data(page=page)
    await call.message.edit_text(f"Выебите блюдо)\nСтраница: {page+1}/{lenth}", reply_markup=food_by_category(data=category, page=page, file=file))


async def add_to_basket(call: CallbackQuery, state: FSMContext):
    food = call.data.split(':')[1]
    data = await state.get_data()
    category = data.get('category')
    page = data.get('page')
    file_rest = data.get('file')
    with open(f"{file_rest}.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        file.close()
        for categorys in vkusochka_menu:
            if str(vkusochka_menu[categorys][0]) == str(category):
                choosen_category = categorys
        for item in vkusochka_menu[choosen_category][1::][page]:
            if str(item[0][0]) == str(food):
                with open('basket.json', 'r', encoding='utf-8') as basket:
                    basket_old = json.load(basket)
                    basket.close()
                with open('basket.json', 'w', encoding='utf-8') as basket:
                    if str(call.from_user.username) in basket_old.keys():
                        pass
                    else:
                        basket_old[str(call.from_user.username)] = dict()
                    if file_rest in basket_old[str(call.from_user.username)].keys() and basket_old[str(call.from_user.username)][file_rest] is not None:
                        pass
                    else:
                        basket_old[str(call.from_user.username)][file_rest] = list()
                    basket_old[str(call.from_user.username)][file_rest].append([item[0][1], re.findall(r'\d+', item[1])])
                    basket.write(json.dumps(basket_old, ensure_ascii=False))
                    await call.answer(text=f'{item[0][1]} добавлено в корзину', show_alert=True)


async def delivery_restaraunts_category_back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file = data.get('file')
    await call.message.edit_text("Выбирай категорию нахуй", reply_markup=sets_by_restaraunt(file))
    await state.set_state(MenuStateVkusochka.Q1)


async def make_delivery_back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
    await state.finish()


async def show_spends(call: CallbackQuery):
    with open('clients_summ_spend.json', 'r', encoding='utf-8') as file:
        history = json.load(file)
    trigger = 0
    for clients in history:
        if str(clients) == str(call.from_user.username):
            trigger = 1
            await call.answer(f"За все время вы заказали на {history[clients]} рублей!", show_alert=True)
    if trigger == 0:
        await call.answer("Пока что вы не завершали заказов через Бота", show_alert=True)


async def delivery_start(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Главное меню", reply_markup=menu_keyboard)
    await state.finish()


async def change_sub_status(call: CallbackQuery):
    with open('subscription.json', 'r', encoding='utf-8') as f:
        subscribers = json.load(f)
        f.close()
        for subscriber in subscribers:
            if str(subscriber) == str(call.from_user.id):
                if subscribers[subscriber]:
                    subscribers[subscriber] = False
                    await call.answer(text="Подписка отключена", show_alert=True)
                else:
                    subscribers[subscriber] = True
                    await call.answer(text="Подписка подключена", show_alert=True)
                with open("subscription.json", "w", encoding='utf-8') as file:
                    json.dump(subscribers, file, ensure_ascii=False)


def register_make_delivery(dp: Dispatcher):
    dp.register_callback_query_handler(change_sub_status, menu_callback.filter(choiсe="disconnect_me"), state=None)
    dp.register_callback_query_handler(show_spends, menu_callback.filter(choiсe="my_spend"), state=None)
    dp.register_callback_query_handler(make_delivery_back, restauranta_callback.filter(choose="back"), state=MenuStateVkusochka.Q4)
    dp.register_callback_query_handler(make_delivery, menu_callback.filter(choiсe="start_delivery"), state=None)
    dp.register_callback_query_handler(make_delivery_back, basket_callback.filter(step="back"), state=Basket.W1)
    dp.register_callback_query_handler(check_basket, basket_callback.filter(step="back"), state=Basket.W2)
    dp.register_callback_query_handler(make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="inicialize"), state=MenuStateVkusochka.Q3)
    dp.register_callback_query_handler(dont_make_delivery_restaraunts, inicialization_delivery_callback.filter(choiсe="no_inicialize"), state=MenuStateVkusochka.Q3)
    dp.register_callback_query_handler(delivery_end, basket_callback.filter(step="clear_basket"), state=Basket.W1)
    dp.register_callback_query_handler(client_basket_clear, basket_callback.filter(step="clear_client_basket"), state=Basket.W1)
    dp.register_callback_query_handler(client_basket_edit, basket_callback.filter(step="edit_basket"), state=Basket.W1)
    dp.register_callback_query_handler(check_basket, menu_callback.filter(choiсe="basket"), state=None)
    dp.register_callback_query_handler(choose_restaraunt, menu_vkusochka_callback.filter(category="back_to_restaurants"), state=MenuStateVkusochka.Q1)
    dp.register_callback_query_handler(delivery_restaraunts_category_back, menu_vkusochka_callback.filter(category="back_to_sets"), state=MenuStateVkusochka.Q2)
    dp.register_callback_query_handler(delivery_restaraunts_category_left, menu_vkusochka_callback.filter(category="chel_peremestilsya_vlevo"), state=MenuStateVkusochka.Q2)
    dp.register_callback_query_handler(delivery_restaraunts_category_right, menu_vkusochka_callback.filter(category="chel_peremestilsya_vpravo"), state=MenuStateVkusochka.Q2)
    dp.register_callback_query_handler(add_to_basket, state=MenuStateVkusochka.Q2)
    dp.register_callback_query_handler(delivery_restaraunts_category, state=MenuStateVkusochka.Q1)
    dp.register_callback_query_handler(choose_category, state=MenuStateVkusochka.Q4)
    dp.register_callback_query_handler(delete_from_basket, state=Basket.W2)
    dp.register_callback_query_handler(choose_restaraunt, state=MenuStateVkusochka.Q3)

