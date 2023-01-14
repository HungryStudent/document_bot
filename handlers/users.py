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
from handlers.texts import *
from utils import db
from config import admin_ids


class UserType(Enum):
    student = 1
    teacher = 2



@dp.message_handler(commands='start')
async def start_message(message: Message):
    if message.from_user.id in admin_ids:
        await message.answer(texts.admin_hello_text, reply_markup=admin_kb.menu)
