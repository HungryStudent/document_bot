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
from handlers.texts import *
from utils import db
from config import admin_ids


@dp.message_handler(lambda m: m.from_user.id in admin_ids, text="Изменить поставщика")
async def start_change_provider(message: Message):
    await message.answer(texts.Provider.enter_name, reply_markup=admin_kb.cancel)
    await states.ChangeProvider.enter_name.set()


@dp.message_handler(text="Отмена")
async def enter_name(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input, reply_markup=admin_kb.menu)


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

    await message.answer(texts.Provider.enter_ogrn)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_ogrn)
async def enter_ogrn(message: Message, state: FSMContext):
    await state.update_data(ogrn=message.text)

    await message.answer(texts.Provider.enter_payment)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_payment)
async def enter_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)

    await message.answer(texts.Provider.enter_bank)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_bank)
async def enter_bank(message: Message, state: FSMContext):
    await state.update_data(bank=message.text)

    await message.answer(texts.Provider.enter_correspondent)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_correspondent)
async def enter_correspondent(message: Message, state: FSMContext):
    await state.update_data(correspondent=message.text)

    await message.answer(texts.Provider.enter_bik)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_bik)
async def enter_bik(message: Message, state: FSMContext):
    await state.update_data(bik=message.text)

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

    await message.answer(texts.Provider.enter_director)
    await states.ChangeProvider.next()


@dp.message_handler(state=states.ChangeProvider.enter_director)
async def enter_director(message: Message, state: FSMContext):
    await state.update_data(director=message.text)
    provider_data = await state.get_data()
    await states.ChangeProvider.next()
    await message.answer(texts.Provider.check.format(**provider_data), reply_markup=admin_kb.accept_new_provider)


@dp.callback_query_handler(Text(startswith="new_provider"), state=states.ChangeProvider.check)
async def change_provider(call: CallbackQuery, state: FSMContext):
    status = call.data[13:]
    if status == "accept":
        provider_data = await state.get_data()
        db.change_provider(provider_data)
        await call.message.answer(texts.Provider.finish, reply_markup=admin_kb.menu)
    elif status == "cancel":
        await call.message.answer(texts.cancel_input, reply_markup=admin_kb.menu)

    await state.finish()
    await call.message.delete()
