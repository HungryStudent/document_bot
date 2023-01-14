from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Изменить поставщика"))

accept_new_provider = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Обновить", callback_data="new_provider_accept"),
    InlineKeyboardButton("Отмена", callback_data="new_provider_cancel"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))
