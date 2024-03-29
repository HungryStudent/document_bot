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


@dp.message_handler(lambda m: m.from_user.id in admin_ids, commands="addbank")
@dp.message_handler(lambda m: m.from_user.id in admin_ids, text="Банки")
async def show_banks_menu(message: Message):
    await message.answer(texts.banks_menu, reply_markup=admin_kb.get_banks_menu())


@dp.callback_query_handler(admin_kb.bank_admin_data.filter())
async def show_bank(call: CallbackQuery, callback_data: dict):
    bank = db.get_bank(callback_data["id"])
    await call.message.answer(
        f"{bank['provider_bank_name']}, БИК {bank['provider_bik']}, счёт {bank['provider_payment']}, кор. счёт {bank['provider_correspondent']}",
        reply_markup=admin_kb.get_bank(bank["id"]))
    await call.answer()


@dp.callback_query_handler(Text(startswith="delete_bank"))
async def delete_bank(call: CallbackQuery):
    db.delete_bank(call.data.split(":")[1])
    await call.message.edit_text("Банк удален")


@dp.message_handler(lambda m: m.from_user.id in admin_ids, state="*", text="Отмена")
async def cancel_change_provider(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input)


@dp.callback_query_handler(text="add_bank")
async def start_add_bank(call: CallbackQuery):
    await states.AddBank.enter_name.set()
    await call.message.answer(texts.Bank.enter_name, reply_markup=admin_kb.cancel)
    await call.answer()


@dp.message_handler(state=states.AddBank.enter_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(texts.Bank.enter_bik)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
    await states.AddBank.next()


@dp.message_handler(state=states.AddBank.enter_bik)
async def enter_bik(message: Message, state: FSMContext):
    await state.update_data(bik=message.text)

    await message.answer(texts.Bank.enter_payment)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
    await states.AddBank.next()


@dp.message_handler(state=states.AddBank.enter_payment)
async def enter_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)

    await message.answer(texts.Bank.enter_correspondent)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
    await states.AddBank.next()


@dp.message_handler(state=states.AddBank.enter_correspondent)
async def enter_correspondent(message: Message, state: FSMContext):
    await state.update_data(correspondent=message.text)
    bank_data = await state.get_data()
    db.add_bank(bank_data)
    await message.answer(texts.Bank.finish)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
    await state.finish()
