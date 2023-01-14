from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeProvider(StatesGroup):
    enter_name = State()
    enter_address = State()
    enter_inn = State()
    enter_ogrn = State()
    enter_payment = State()
    enter_bank = State()
    enter_correspondent = State()
    enter_bik = State()
    enter_phone = State()
    enter_email = State()
    enter_director = State()
    check = State()