import datetime
import json
import os
import sys
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback, \
    inicialization_delivery_callback, basket_callback, restauranta_callback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test_parser import VkusnoITochka_parser


def basket_back(client_id, client_username):
    buttons_list = []
    with open('who_start_delivery.json', 'r', encoding='utf-8') as file:
        client_deliver = json.load(file)
        deliver_id = client_deliver['customer'][0]
        if str(deliver_id) == str(client_id) and client_deliver['is_deliver_start']:
            buttons_list.append([
                InlineKeyboardButton(text="Сделать заказ и очистить корзину 📦", callback_data=basket_callback.new(step="clear_basket"))
            ])
        if client_deliver['is_deliver_start']:
            with open('basket.json', 'r', encoding='utf-8') as file:
                basket = json.load(file)
                for people in basket:
                    if people == client_username:
                        buttons_list.append([InlineKeyboardButton(text="Очистить свою корзину 🗑️", callback_data=basket_callback.new(step="clear_client_basket"))])
                        buttons_list.append([InlineKeyboardButton(text="Редактировать свою корзину 🖊", callback_data=basket_callback.new(step="edit_basket"))])
        buttons_list.append([InlineKeyboardButton(text="Назад ↩", callback_data=basket_callback.new(step="back"))])
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)


def menu_keyboard(client_id):
    with open('subscription.json', 'r', encoding='utf-8') as file:
        subsribers = json.load(file)
    if str(client_id) in subsribers and subsribers[str(client_id)]:
        add_button = [InlineKeyboardButton(text="Рассылка подключена ✅", callback_data=menu_callback.new(choiсe="disconnect_me"))]
    else:
        add_button = [InlineKeyboardButton(text="Рассылка не подключена ❌", callback_data=menu_callback.new(choiсe="disconnect_me"))]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Заказать покушать 😋", callback_data=menu_callback.new(choiсe="start_delivery"))
            ],
            [
                InlineKeyboardButton(text="Просмотреть общую корзину 🛒", callback_data=menu_callback.new(choiсe="basket"))
            ],
            [
                InlineKeyboardButton(text="Мои траты 📊", callback_data=menu_callback.new(choiсe="my_spend"))
            ],
            add_button
        ]
)


def choose_restaraunt_keyboard():
    with open("restaurants.json", "r", encoding="utf-8") as file:
        restaurants = json.load(file)
    keyboard_data = []
    for restaurant in restaurants['restaurants']:
        keyboard_data.append([InlineKeyboardButton(text=f"{restaurant}", callback_data=restauranta_callback.new(choose=f"{restaurants['restaurants'].index(restaurant)}"))])
    keyboard_data.append([InlineKeyboardButton(text='Назад ↩', callback_data=restauranta_callback.new(choose='back'))])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_data)


inicialization_delivery = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, я хочу заказать доставку ✅", callback_data=inicialization_delivery_callback.new(choiсe="inicialize"))
        ],
        [
            InlineKeyboardButton(text="Нет уж, подожду ❌", callback_data=inicialization_delivery_callback.new(choiсe="no_inicialize"))
        ]
    ]
)


def edit_basket_keyboard(user_name):
    with open('basket.json', 'r', encoding='utf-8') as file:
        basket = json.load(file)
    keyboard_data = []
    for rest in basket[user_name]:
        for client_food in basket[user_name][rest]:
            keyboard_data.append([InlineKeyboardButton(text=str(client_food[0] + " " + str(client_food[1][0]) + "р"), callback_data=basket_callback.new(step=str(basket[user_name][rest].index(client_food)) + "/" + str(rest)))])
    keyboard_data.append([InlineKeyboardButton(text='Назад ↩', callback_data=basket_callback.new(step='back'))])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_data)


def sets_by_restaraunt(file):
    menu_vkusocka_kb = []
    p = VkusnoITochka_parser()
    try:
        last_modified = time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getmtime(f"{file}.json"))))
        if str(last_modified) != str(datetime.date.today()):
            p.get_vit_menu()
            p.get_restaurant_menu()
            p.parse_online_restaurants()
    except:
        p.get_vit_menu()
        p.get_restaurant_menu()
        p.parse_online_restaurants()

    with open(f"{file}.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for category in vkusochka_menu:
            if len(vkusochka_menu[category]) > 1 and category:
                menu_vkusocka_kb.append([InlineKeyboardButton(text=category, callback_data=menu_vkusochka_callback.new(category=vkusochka_menu[category][0]))])
        menu_vkusocka_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_kb)
        back_button = InlineKeyboardButton(text="Назад ↩", callback_data=menu_vkusochka_callback.new(category="back_to_restaurants"))
        menu_vkusocka_keyboard.insert(back_button)
        return menu_vkusocka_keyboard


def food_by_category(data, page, file):
    menu_vkusocka_in_kb = []
    step = int(page)
    with open(f"{file}.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for ct in vkusochka_menu:
            if str(vkusochka_menu[ct][0]) == str(data):
                category = ct
        for zxc in vkusochka_menu[category][1::][step]:
            menu_vkusocka_in_kb.append([InlineKeyboardButton(text=f'{zxc[0][1]} {zxc[1]}', callback_data=menu_vkusochka_callback.new(category=zxc[0][0]))])
        left_button = InlineKeyboardButton(text="←", callback_data=menu_vkusochka_callback.new(category="chel_peremestilsya_vlevo"))
        back_button = InlineKeyboardButton(text="Назад ↩", callback_data=menu_vkusochka_callback.new(category="back_to_sets"))
        right_button = InlineKeyboardButton(text="→", callback_data=menu_vkusochka_callback.new(category="chel_peremestilsya_vpravo"))
        last_button = [left_button, back_button, right_button]
        menu_vkusocka_in_kb.append(last_button)
        food_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_in_kb)
        return food_keyboard
