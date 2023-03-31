from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
from aiogram.utils.exceptions import BotKicked

from handlers import texts
from create_bot import dp, log
import states.admin as states
from datetime import date, timedelta
import keyboards.admin as admin_kb
from utils import db
from config import admin_ids


@dp.message_handler(lambda m: m.from_user.id in admin_ids, commands="setcompany")
@dp.message_handler(lambda m: m.from_user.id in admin_ids, text="Изменить поставщика")
async def start_change_provider(message: Message):
    await message.answer(texts.Provider.enter_name, reply_markup=admin_kb.cancel)
    await states.ChangeProvider.enter_name.set()


@dp.message_handler(lambda m: m.from_user.id in admin_ids, state="*", text="Отмена")
async def cancel_change_provider(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input)


@dp.message_handler(state=states.ChangeProvider.enter_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(texts.Provider.enter_address)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_address)
async def enter_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    await message.answer(texts.Provider.enter_inn)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_inn)
async def enter_inn(message: Message, state: FSMContext):
    await state.update_data(inn=message.text)

    await message.answer("Введите КПП")
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_kpp)
async def enter_kpp(message: Message, state: FSMContext):
    await state.update_data(kpp=message.text)

    await message.answer(texts.Provider.enter_ogrn)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_ogrn)
async def enter_ogrn(message: Message, state: FSMContext):
    await state.update_data(ogrn=message.text)

    await message.answer(texts.Provider.enter_phone)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await message.answer(texts.Provider.enter_email)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    await message.answer("Введите имя бухгалтера")
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_accountant)
async def enter_accountant(message: Message, state: FSMContext):
    await state.update_data(accountant=message.text)

    await message.answer("Введите должность")
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_role)
async def enter_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)

    await message.answer("Введите должность в родительном падеже")
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_role_parent)
async def enter_role_parent(message: Message, state: FSMContext):
    await state.update_data(role_parent=message.text)

    await message.answer("Введите ФИО")
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_fio)
async def enter_fio(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 3:
        await message.answer(texts.CreateDocument.fio_error)
        return
    await state.update_data(fio=message.text)

    await message.answer("Введите ФИО в родительном падеже")
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_fio_parent)
async def enter_fio_parent(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 3:
        await message.answer(texts.CreateDocument.fio_error)
        return
    await state.update_data(fio_parent=message.text)

    data = await state.get_data()
    await message.answer(texts.Provider.check.format(**data), reply_markup=admin_kb.accept_new_provider)
    await states.ChangeProvider.next()


@dp.callback_query_handler(Text(startswith="new_provider"), state=states.ChangeProvider.check)
async def change_provider(call: CallbackQuery, state: FSMContext):
    status = call.data[13:]
    if status == "accept":
        provider_data = await state.get_data()
        db.change_provider(provider_data)
        await call.message.answer(texts.Provider.finish)
    elif status == "cancel":
        await call.message.answer(texts.cancel_input)

    await state.finish()
    await call.message.delete()
