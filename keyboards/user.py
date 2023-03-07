from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils import db

type_product_names = ["шт.", "кг.", "м.", "км.", "м²", "м3", "тн.", "п.м.", "уп.", "пара"]

bank_data = CallbackData("bank", "id")

add_product = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Добавить", callback_data="add_product"))
product_menu = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Добавить", callback_data="add_product"),
                                                     (InlineKeyboardButton("Завершить",
                                                                           callback_data="finish_product")))

doc_type = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("DOCX", callback_data="doc_type:1"),
                                                 InlineKeyboardButton("PDF", callback_data="doc_type:2"))

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Создать договор"),
                                                                  KeyboardButton("Создать КП"),
                                                                  KeyboardButton("Изменить свои данные"))

org_type = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Юр. лицо", callback_data="org_type:1"),
                                                 InlineKeyboardButton("ИП", callback_data="org_type:2"))
nds = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton("0%", callback_data="nds:0"),
                                            InlineKeyboardButton("10%", callback_data="nds:10"),
                                            InlineKeyboardButton("20%", callback_data="nds:20"))
cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

type_product = InlineKeyboardMarkup(row_width=3)
for i in range(len(type_product_names)):
    type_product.insert(InlineKeyboardButton(type_product_names[i], callback_data=f"type_product:{i}"))


def get_banks():
    kb = InlineKeyboardMarkup(row_width=1)
    banks = db.get_banks()
    for bank in banks:
        kb.add(InlineKeyboardButton(bank["name"], callback_data=bank_data.new(bank["id"])))
    return kb
