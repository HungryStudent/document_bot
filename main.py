from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.utils import executor

from config import admin_ids
from create_bot import dp, bot
from utils import db
from handlers import users
from handlers import admin


async def on_startup(_):
    await bot.set_my_commands([BotCommand("/createoffer", "Создать КП"),
                               BotCommand("/createcontract", "Создать договор"),
                               BotCommand("/correctuserdata", "Изменить свои данные")], BotCommandScopeDefault())
    for admin_id in admin_ids:
        await bot.set_my_commands([BotCommand("/createoffer", "Создать КП"),
                                   BotCommand("/createcontract", "Создать договор"),
                                   BotCommand("/correctuserdata", "Изменить свои данные"),
                                   BotCommand("/setcompany", "Изменить поставщика"),
                                   BotCommand("/addbank", "Добавить счет (банки)")
                                   ], BotCommandScopeChat(admin_id))
    db.start()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
