from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateDocument(StatesGroup):
    enter_provider_bank = State()
    enter_org_type = State()
    enter_nds = State()
    enter_number = State()
    enter_inn = State()
    enter_role = State()
    enter_role_parent = State()
    enter_name = State()
    enter_kpp = State()
    enter_bank_name = State()
    enter_bik = State()
    enter_payment = State()
    enter_correspondent = State()
    enter_ogrn = State()
    enter_address = State()
    enter_fio = State()
    enter_fio_parent = State()
    enter_phone = State()
    enter_email = State()
    enter_prepaid_expense = State()
    enter_delivery_address = State()
    enter_product = State()
    enter_name_product = State()
    enter_count_product = State()
    enter_type_product = State()
    enter_price_product = State()
    enter_doc_type = State()


class ChangeMyInfo(StatesGroup):
    fi = State()
    role = State()
    email = State()
    number = State()
    office_number = State()
    site = State()


class CreateKP(StatesGroup):
    number = State()
    nds = State()
    product = State()
    name_product = State()
    count_product = State()
    type_product = State()
    price_product = State()