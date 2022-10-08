import datetime
import json
import os
import sys
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback, \
    inicialization_delivery_callback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test_parser import VkusnoITochka_parser


basket_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data=menu_callback.new(choiсe="start_delivery"))
        ]
    ]
)

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
            InlineKeyboardButton(text="Отключить рассылку", callback_data=menu_callback.new(choiсe="connect_me"))
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

    try:
        last_modified = time.strftime("%Y-%m-%d", time.strptime(time.ctime(os.path.getmtime("menu.json"))))
        if str(last_modified) != str(datetime.date.today()):         #проерка, если сегодня изменялся файл (парсился), то еще раз его парсить не надо
            VkusnoITochka_parser().get_vit_menu()

    except:
        VkusnoITochka_parser().get_vit_menu()

    with open("menu.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for category in vkusochka_menu:
            if len(vkusochka_menu[category]) > 1 and category:
                menu_vkusocka_kb.append([InlineKeyboardButton(text=category, callback_data=menu_vkusochka_callback.new(category=vkusochka_menu[category][0]))])
        menu_vkusocka_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_kb)
        back_button = InlineKeyboardButton(text="Назад", callback_data=menu_vkusochka_callback.new(category="back"))
        menu_vkusocka_keyboard.insert(back_button)
        return menu_vkusocka_keyboard


def food_by_category(data):
    menu_vkusocka_in_kb = []
    with open("menu.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for ct in vkusochka_menu:
            if str(vkusochka_menu[ct][0]) == str(data):
                category = ct
        for zxc in vkusochka_menu[category][1::]:
            menu_vkusocka_in_kb.append([InlineKeyboardButton(text=f'{zxc[0][1]} {zxc[1]}', callback_data=menu_vkusochka_callback.new(category=zxc[0][0]))])
        back_button = InlineKeyboardButton(text="Назад", callback_data=menu_vkusochka_callback.new(category="back"))
        food_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_in_kb)
        food_keyboard.insert(back_button)
        return food_keyboard
