from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateDocument(StatesGroup):
    enter_number = State()
    enter_name = State()
    enter_address = State()
    enter_inn = State()
    enter_kpp = State()
    enter_ogrn = State()
    enter_payment = State()
    enter_bank_name = State()
    enter_correspondent = State()
    enter_bik = State()
    enter_phone = State()
    enter_email = State()
    enter_role = State()
    enter_role_parent = State()
    enter_fio = State()
    enter_fio_parent = State()
    enter_provider_bank = State()