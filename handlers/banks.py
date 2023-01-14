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


@dp.message_handler(lambda m: m.from_user.id in admin_ids, text="Банки")
async def show_banks_menu(message: Message):
    await message.answer(texts.banks_menu, reply_markup=admin_kb.get_banks_menu())


@dp.message_handler(state="*", text="Отмена")
async def cancel_change_provider(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input, reply_markup=admin_kb.menu)


@dp.callback_query_handler(text="add_bank")
async def start_add_bank(call: CallbackQuery):
    await states.AddBank.enter_name.set()
    await call.message.answer(texts.Bank.enter_name, reply_markup=admin_kb.cancel)
    await call.answer()

@dp.message_handler(state=states.AddBank.enter_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(texts.Bank.enter_bik)
    await states.AddBank.next()


@dp.message_handler(state=states.AddBank.enter_bik)
async def enter_bik(message: Message, state: FSMContext):
    await state.update_data(bik=message.text)

    await message.answer(texts.Bank.enter_payment)
    await states.AddBank.next()


@dp.message_handler(state=states.AddBank.enter_payment)
async def enter_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)

    await message.answer(texts.Bank.enter_correspondent)
    await states.AddBank.next()


@dp.message_handler(state=states.AddBank.enter_correspondent)
async def enter_correspondent(message: Message, state: FSMContext):
    await state.update_data(correspondent=message.text)
    bank_data = await state.get_data()
    db.add_bank(bank_data)
    await message.answer(texts.Bank.finish, reply_markup=admin_kb.menu)
    await states.AddBank.next()
