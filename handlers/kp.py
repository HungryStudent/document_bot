from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import keyboards.admin as admin_kb
import keyboards.user as user_kb
from config import admin_ids
from create_bot import dp
from handlers import texts
from states.user import ChangeMyInfo
from utils import db
from utils import doc_gen


@dp.message_handler(text="Создать КП")
async def create_kp(message: Message):
    user = db.get_user(message.from_user.id)
    name = doc_gen.get_kp(user)

    if message.from_user.id in admin_ids:
        kb = admin_kb.menu
    else:
        kb = user_kb.menu

    await message.answer_document(open(name + ".docx", "rb"), caption="КП",
                                  reply_markup=kb)


@dp.message_handler(text="Изменить свои данные")
async def change_my_info(message: Message):
    await message.answer("Введите ФИ", reply_markup=user_kb.cancel)
    await ChangeMyInfo.fi.set()


@dp.message_handler(state=ChangeMyInfo.fi)
async def enter_fi(message: Message, state: FSMContext):
    await state.update_data(fi=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите должность")


@dp.message_handler(state=ChangeMyInfo.role)
async def enter_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите e-mail")


@dp.message_handler(state=ChangeMyInfo.email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите номер телефона")


@dp.message_handler(state=ChangeMyInfo.number)
async def enter_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите номер офиса")


@dp.message_handler(state=ChangeMyInfo.office_number)
async def enter_office_number(message: Message, state: FSMContext):
    await state.update_data(office_number=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите название сайта")


@dp.message_handler(state=ChangeMyInfo.site)
async def enter_site(message: Message, state: FSMContext):
    await state.update_data(site=message.text)
    data = await state.get_data()
    db.change_my_info(data, message.from_user.id)

    if message.from_user.id in admin_ids:
        kb = admin_kb.menu
    else:
        kb = user_kb.menu

    await message.answer(f"""Ваши персональные данные обновлены:
ФИ {data['fi']}
Должность {data['role']}
E-mail {data['email']}
Номер телефона {data['number']}
Номер офиса {data['office_number']}
Название сайта {data['site']}""", reply_markup=kb)
    await state.finish()
