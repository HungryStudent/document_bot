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


@dp.callback_query_handler(Text(startswith="user"))
async def check_user(call: CallbackQuery):
    if call.data.split(":")[1] == "approve":
        await call.message.edit_reply_markup(reply_markup=admin_kb.approve)
        db.activate_user(call.data.split(":")[2])
        await call.bot.send_message(call.data.split(":")[2], "Аккаунт активирован")
    elif call.data.split(":")[1] == "reject":
        await call.message.edit_reply_markup(reply_markup=admin_kb.reject)
