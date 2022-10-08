from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import menu_callback, menu_vkusochka_callback, inicialization_delivery_callback


import os, re, sys, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test_parser import VkusnoITochka_parser


menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заказать покушать", callback_data=menu_callback.new(choiсe="start_delivery"))
        ],
        [
            InlineKeyboardButton(text="Мои траты", callback_data=menu_callback.new(choiсe="my_spend"))
        ],
        [
            InlineKeyboardButton(text="Отключить рассылку", callback_data=menu_callback.new(choiсe="connect_me"))
        ]
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
    VkusnoITochka_parser().get_menu()
    with open("menu.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for category in vkusochka_menu:
            if vkusochka_menu[category] and category:
                menu_vkusocka_kb.append([InlineKeyboardButton(text=category, callback_data=menu_vkusochka_callback.new(category=vkusochka_menu[category][0]))])
        menu_vkusocka_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_kb)
        back_button = InlineKeyboardButton(text="Назад", callback_data=menu_vkusochka_callback.new(category="back"))
        menu_vkusocka_keyboard.insert(back_button)
        return menu_vkusocka_keyboard


def sets_by_restaraunt_back():
    menu_vkusocka_kb = []
    with open("menu.json", "r", encoding='utf-8') as file:
        vkusochka_menu = json.load(file)
        for category in vkusochka_menu:
            if vkusochka_menu[category] and category:
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
        for zxc in vkusochka_menu[category]:
            if zxc == 0:
                pass
            else:
                menu_vkusocka_in_kb.append(
                    [InlineKeyboardButton(text=f'{zxc[0][1]} {zxc[1]}', callback_data=menu_vkusochka_callback.new(category=zxc[0][0]))])
        back_button = InlineKeyboardButton(text="Назад", callback_data=menu_vkusochka_callback.new(category="back"))
        food_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_vkusocka_in_kb)
        food_keyboard.insert(back_button)
        return food_keyboard
