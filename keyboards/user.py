from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils import db

bank_data = CallbackData("bank", "id")

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Создать договор"))


cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

def get_banks():
    kb = InlineKeyboardMarkup(row_width=1)
    banks = db.get_banks()
    for bank in banks:
        kb.add(InlineKeyboardButton(bank["name"], callback_data=bank_data.new(bank["id"])))
    return kb
