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
    await message.answer("Приветик)\nГлавное меню", reply_markup=menu_keyboard)


def register_delivery_start(dp: Dispatcher):
    dp.register_message_handler(delivery_start, commands=["menu", "start"], state="*")