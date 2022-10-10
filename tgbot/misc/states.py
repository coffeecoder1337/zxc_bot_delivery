from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuStateVkusochka(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class Basket(StatesGroup):
    W1 = State()
    W2 = State()