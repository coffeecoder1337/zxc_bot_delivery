import datetime
import json
import os
import sys
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback, \
    inicialization_delivery_callback, basket_callback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test_parser import VkusnoITochka_parser


def basket_back(client_id):
    buttons_list = [
            [
                InlineKeyboardButton(text="Назад", callback_data=basket_callback.new(step="back"))
            ]
        ]
    with open('who_start_delivery.json', 'r', encoding='utf-8') as file:
        client_deliver = json.load(file)
        deliver_id = client_deliver['customer'][0]
        if str(deliver_id) == str(client_id):
            buttons_list.append([
                InlineKeyboardButton(text="Сделать заказ и очистить корзину", callback_data=basket_callback.new(step="clear_basket"))
            ])
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)


menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заказать покушать", callback_data=menu_callback.new(choiсe="start_delivery"))
        ],
        [
            InlineKeyboardButton(text="Просмотреть общую корзину", callback_data=menu_callback.new(choiсe="basket"))
        ],
        [
            InlineKeyboardButton(text="Мои траты", callback_data=menu_callback.new(choiсe="my_spend"))
        ],
        [
            InlineKeyboardButton(text="Рассылка", callback_data=menu_callback.new(choiсe="disconnect_me"))
        ],
    ]
)

inicialization_delivery = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, я хочу заказать доставку", callback_data=inicialization_delivery_callback.new(choiсe="inicialize"))
        ],
        [
            InlineKeyboardButton(text="Нет уж, подожду", callback_data=inicialization_delivery_callback.new(choiсe="no_inicialize"))
        ]
    ]
)


def sets_by_restaraunt():
    menu_vkusocka_kb = []
    p = VkusnoITochka_parser()    
    try:
        last_modified = time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getmtime("Вкусно и точка.json"))))
        if str(last_modified) != str(datetime.date.today()):         #проерка, если сегодня изменялся файл (парсился), то еще раз его парсить не надо
            p.get_vit_menu()
            p.get_restaurant_menu()
            p.parse_online_restaurants()


    except:
        p.get_vit_menu()
        p.get_restaurant_menu()
        p.parse_online_restaurants()

    with open("Вкусно и точка.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for category in vkusochka_menu:
            if len(vkusochka_menu[category]) > 1 and category:
                menu_vkusocka_kb.append([InlineKeyboardButton(text=category, callback_data=menu_vkusochka_callback.new(category=vkusochka_menu[category][0]))])
        menu_vkusocka_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_kb)
        back_button = InlineKeyboardButton(text="Назад", callback_data=menu_vkusochka_callback.new(category="back"))
        menu_vkusocka_keyboard.insert(back_button)
        return menu_vkusocka_keyboard


def food_by_category(data, page):
    menu_vkusocka_in_kb = []
    step = int(page)
    with open("Вкусно и точка.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for ct in vkusochka_menu:
            if str(vkusochka_menu[ct][0]) == str(data):
                category = ct
        for zxc in vkusochka_menu[category][1::][step]:
            menu_vkusocka_in_kb.append([InlineKeyboardButton(text=f'{zxc[0][1]} {zxc[1]}', callback_data=menu_vkusochka_callback.new(category=zxc[0][0]))])
        left_button = InlineKeyboardButton(text="←", callback_data=menu_vkusochka_callback.new(category="chel_peremestilsya_vlevo"))
        back_button = InlineKeyboardButton(text="Назад", callback_data=menu_vkusochka_callback.new(category="back"))
        right_button = InlineKeyboardButton(text="→", callback_data=menu_vkusochka_callback.new(category="chel_peremestilsya_vpravo"))
        last_button = [left_button, back_button, right_button]
        menu_vkusocka_in_kb.append(last_button)
        food_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_in_kb)
        return food_keyboard
