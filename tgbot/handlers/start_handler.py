import json

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline.menu_buttons import menu_keyboard


async def delivery_start(message: Message, state: FSMContext):
    with open("subscription.json", "r", encoding='utf-8') as file:
        all_subs = json.load(file)
        file.close()
        is_subscriber = False
        for sub in all_subs:
            if str(sub) == str(message.from_id) and all_subs[sub]:
                is_subscriber = True
        if not is_subscriber:
            all_subs[message.from_id] = True
            with open('subscription.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(all_subs, ensure_ascii=False))
    await state.finish()
    await message.answer("🧾 Главное меню 🧾", reply_markup=menu_keyboard(message.from_id))


async def delivery_info(message: Message):
    await message.answer('''Привет, я бот-помощник. Я помогу вам заказать доставку еды прямо в офис. 🚚
Используйте команду /start или /menu для того чтобы открыть меню с ресторанами и выбрать нужные блюда.
Добавьте их в общую корзину и оформите доставку, а я оповещу ваших коллег об этом.
❗После того как инициатор доставки закроет корзину, всем будет выслано сообщение, где сказано, сколько они должны инициатору. А у инициатора будет сформирован общий чек, по которому он будет должен сделать заказ.
❗ Инициатор - тот, кто начал доставку, он всегда только один.
❗ Для того, чтобы получать оповещения об инициализации доставки, вы должны быть подписаны на рассылку. Подписка/ отписка происходит при нажатии на кнопку "Рассылка подключена"''')


def register_delivery_start(dp: Dispatcher):
    dp.register_message_handler(delivery_start, commands=["menu", "start"], state="*")
    dp.register_message_handler(delivery_info, commands=["info"], state="*")