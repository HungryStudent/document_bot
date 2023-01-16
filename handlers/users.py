from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.utils.exceptions import BotKicked

from handlers import texts
from create_bot import dp, log
from datetime import date, timedelta
import keyboards.admin as admin_kb
import keyboards.user as user_kb
from handlers.texts import *
from utils import db
from config import admin_ids
from states import user as states
from utils import doc_gen


class UserType(Enum):
    student = 1
    teacher = 2


@dp.message_handler(commands='start')
async def start_message(message: Message):
    if message.from_user.id in admin_ids:
        await message.answer(texts.admin_hello_text, reply_markup=admin_kb.menu)
    else:
        await message.answer(texts.hello, reply_markup=user_kb.menu)


@dp.message_handler(text="Создать договор")
async def start_create_document(message: Message):
    await states.CreateDocument.enter_number.set()
    await message.answer(texts.CreateDocument.enter_number)


@dp.message_handler(state="*", text="Отмена")
async def cancel_user(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input, reply_markup=user_kb.menu)


@dp.message_handler(state=states.CreateDocument.enter_number)
async def enter_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_name)


@dp.message_handler(state=states.CreateDocument.enter_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_address)


@dp.message_handler(state=states.CreateDocument.enter_address)
async def enter_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_inn)


@dp.message_handler(state=states.CreateDocument.enter_inn)
async def enter_inn(message: Message, state: FSMContext):
    await state.update_data(inn=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_kpp)


@dp.message_handler(state=states.CreateDocument.enter_kpp)
async def enter_kpp(message: Message, state: FSMContext):
    await state.update_data(kpp=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_ogrn)


@dp.message_handler(state=states.CreateDocument.enter_ogrn)
async def enter_ogrn(message: Message, state: FSMContext):
    await state.update_data(ogrn=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_payment)


@dp.message_handler(state=states.CreateDocument.enter_payment)
async def enter_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_bank_name)


@dp.message_handler(state=states.CreateDocument.enter_bank_name)
async def enter_bank_name(message: Message, state: FSMContext):
    await state.update_data(bank_name=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_correspondent)


@dp.message_handler(state=states.CreateDocument.enter_correspondent)
async def enter_correspondent(message: Message, state: FSMContext):
    await state.update_data(correspondent=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_bik)


@dp.message_handler(state=states.CreateDocument.enter_bik)
async def enter_bik(message: Message, state: FSMContext):
    await state.update_data(bik=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_phone)


@dp.message_handler(state=states.CreateDocument.enter_phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_email)


@dp.message_handler(state=states.CreateDocument.enter_email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_role)


@dp.message_handler(state=states.CreateDocument.enter_role)
async def enter_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_role_parent)


@dp.message_handler(state=states.CreateDocument.enter_role_parent)
async def enter_role_parent(message: Message, state: FSMContext):
    await state.update_data(role_parent=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_fio)


@dp.message_handler(state=states.CreateDocument.enter_fio)
async def enter_fio(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 3:
        await message.answer(texts.CreateDocument.fio_error)
        return
    await state.update_data(fio=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_fio_parent)


@dp.message_handler(state=states.CreateDocument.enter_fio_parent)
async def enter_fio_parent(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 3:
        await message.answer(texts.CreateDocument.fio_error)
        return
    await state.update_data(fio_parent=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_provider_bank, reply_markup=user_kb.get_banks())


@dp.callback_query_handler(user_kb.bank_data.filter(), state=states.CreateDocument.enter_provider_bank)
async def enter_provider_bank(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(provider_bank=callback_data["id"])

    document_data = await state.get_data()
    document_data = {**document_data, **db.get_bank(document_data["provider_bank"])}
    document_data[
        "fio_iniz"] = f'{document_data["fio"].split(" ")[0]} {document_data["fio"].split(" ")[1][0]}.{document_data["fio"].split(" ")[2][0]}.'
    name = doc_gen.get_docx(document_data)
    await call.message.answer_document(open(name, "rb"), caption=texts.CreateDocument.finish)
    await call.answer()
