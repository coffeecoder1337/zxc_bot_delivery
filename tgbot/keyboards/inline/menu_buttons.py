from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import menu_callback, inicialization_delivery_callback

menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заказать покушать", callback_data=menu_callback.new(choiсe="start_delivery"))
        ],
        [
            InlineKeyboardButton(text="Мои траты", callback_data=menu_callback.new(choiсe="my_spend"))
        ],
        [
            InlineKeyboardButton(text="Подключить рассылку", callback_data=menu_callback.new(choiсe="connect_me"))
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