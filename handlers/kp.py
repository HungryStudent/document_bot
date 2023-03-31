import datetime
from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from number_to_string import get_string_by_number

import keyboards.admin as admin_kb
import keyboards.user as user_kb
from config import admin_ids
from create_bot import dp
from handlers import texts
from states.user import ChangeMyInfo, CreateKP
from utils import doc_gen, text_funcs, db


@dp.message_handler(commands="createoffer")
@dp.message_handler(text="Создать КП")
async def create_kp(message: Message):
    user = db.get_user(message.from_user.id)
    if not user["is_activate"]:
        return

    await message.answer("Введите номер коммерческого предложения")
    await message.delete()
    await CreateKP.number.set()


@dp.message_handler(state=CreateKP.number)
async def kp_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await CreateKP.next()
    await message.answer("Выберите НДС", reply_markup=user_kb.nds)
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()


@dp.callback_query_handler(state=CreateKP.nds)
async def kp_nds(call: CallbackQuery, state: FSMContext):
    await state.update_data(nds=int(call.data.split(":")[1]))
    await state.update_data(products=[])

    await call.message.edit_text("Введите размер аванса", reply_markup=user_kb.prepaid_expense)
    await CreateKP.next()


@dp.callback_query_handler(Text(startswith="prepaid_expense:"), state=CreateKP.enter_prepaid_expense)
async def enter_prepaid_expense(call: CallbackQuery, state: FSMContext):
    await state.update_data(prepaid_expense=call.data.split(":")[1])
    await CreateKP.next()
    await call.message.edit_text("Добавление товаров в спецификацию", reply_markup=user_kb.add_product)


@dp.callback_query_handler(state=CreateKP.product)
async def kp_product(call: CallbackQuery, state: FSMContext):
    if call.data == "finish_product":
        document_data = await state.get_data()
        user = db.get_user(call.from_user.id)
        provider_data = db.get_provider()
        provider_data[
            "provider_fio_iniz"] = f'{provider_data["provider_fio"].split(" ")[0]} ' \
                                   f'{provider_data["provider_fio"].split(" ")[1][0]}.' \
                                   f'{provider_data["provider_fio"].split(" ")[2][0]}.'
        document_data["now_date"] = datetime.datetime.now().strftime("%d.%m.%Y")
        document_data = {**document_data, **user, **provider_data}

        products = document_data["products"]
        document_products = []
        summa = 0
        for product in products:
            if float(product["count"]).is_integer():
                count = int(float(product["count"]))
            else:
                count = product["count"]
            document_products.append({"num": product["num"],
                                      "name": product["name"],
                                      "count": count,
                                      "type": product["type"],
                                      "price": format(round(product["price"], 2), '.2f'),
                                      "cost": format(round(product["count"] * product["price"], 2),
                                                     '.2f')})
            summa += product["cost"]
        document_data["products"] = document_products
        if float(summa).is_integer():
            document_data["summa"] = format(int(summa), '.2f')
            document_data["rubles"] = int(summa)
            document_data["cents"] = "00"
            document_data["cents_text"] = "00 копеек"
        else:
            document_data["summa"] = format(round(summa, 2), '.2f')
            document_data["rubles"] = int(float(document_data["summa"]))

            document_data["cents"] = str(document_data["summa"])[-2:]
            document_data["cents_text"] = str(document_data["cents"]) + " " + text_funcs.get_text_variant(
                int(str(document_data["summa"])[-2:]),
                "копейка, копейки, копеек")
        document_data["rubles_text"] = str(document_data["rubles"]) + " " + text_funcs.get_text_variant(
            int(float(document_data["summa"])),
            "рубль, рубля, рублей")
        document_data["string_summa_text"] = get_string_by_number(summa)
        document_data[
            "summa_text"] = f'{document_data["rubles_text"]} {document_data["cents_text"]} ({document_data["string_summa_text"]})'
        nds_summa = summa * document_data["nds"] * 0.01
        if float(nds_summa).is_integer():
            document_data["nds_summa"] = format(int(nds_summa), '.2f')
            document_data["nds_rubles"] = int(nds_summa)
            document_data["nds_cents"] = "00"
            document_data["nds_cents_text"] = "00 копеек"
        else:
            document_data["nds_summa"] = format(round(nds_summa, 2), '.2f')
            document_data["nds_rubles"] = int(float(document_data["nds_summa"]))
            document_data["nds_cents"] = str(document_data["nds_summa"])[-2:]
            document_data["nds_cents_text"] = str(document_data["nds_cents"]) + " " + text_funcs.get_text_variant(
                int(str(document_data["nds_summa"])[-2:]),
                "копейка, копейки, копеек")

        document_data["nds_rubles_text"] = str(document_data["nds_rubles"]) + " " + text_funcs.get_text_variant(
            int(float(document_data["nds_summa"])),
            "рубль, рубля, рублей")
        document_data["nds_summa_text"] = f'{document_data["nds_rubles_text"]} {document_data["nds_cents_text"]}'
        count = len(document_data["products"])
        document_data["products_count"] = count

        document_data["tbl_contents"] = document_data["products"]
        kp_name = doc_gen.get_kp(document_data)

        await call.message.answer_document(open(kp_name + ".docx", "rb"), caption="Документ создан")
        await call.message.answer_document(open(kp_name + ".pdf", "rb"))
        await state.finish()
        await call.answer()
        await call.message.delete()
        return

    await CreateKP.next()
    await call.message.answer("Укажите Наименование\nПример: Стопорная гайка")
    await call.message.delete()
    await call.answer()


@dp.message_handler(state=CreateKP.name_product)
async def kp_name_product(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)

    await CreateKP.next()
    await message.answer(texts.CreateDocument.enter_count_product)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=CreateKP.count_product)
async def kp_count_product(message: Message, state: FSMContext):
    count_product = message.text.replace(",", ".")
    try:
        await state.update_data(count_product=float(count_product))
    except ValueError:
        await message.answer("Введите число!")
        return

    await CreateKP.next()
    await message.answer("Укажите Наименование\nПример: шт.", reply_markup=user_kb.type_product)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.callback_query_handler(Text(startswith="type_product"), state=CreateKP.type_product)
async def kp_type_product(call: CallbackQuery, state: FSMContext):
    await state.update_data(type_product=int(call.data.split(":")[1]))

    await CreateKP.next()
    await call.message.answer("Укажите Цену за единицу\nПример: 34.55")
    await call.message.delete()
    await call.answer()


@dp.message_handler(state=CreateKP.price_product)
async def kp_price_product(message: Message, state: FSMContext):
    price_product = message.text.replace(",", ".")
    try:
        await state.update_data(price_product=float(price_product))
    except ValueError:
        await message.answer("Введите число!")
        return
    async with state.proxy() as data:
        data["products"].append({"num": len(data["products"]) + 1,
                                 "name": data["name_product"],
                                 "count": data["count_product"],
                                 "type": user_kb.type_product_names[data["type_product"]],
                                 "price": data["price_product"],
                                 "cost": data["count_product"] * data["price_product"]})
        products = ""
        summa = 0
        for product in data["products"]:
            products += texts.CreateDocument.product_info.format(**product)
            summa += product["cost"]
        count = len(data["products"])
        summa = round(summa, 2)
        msg_text = texts.CreateDocument.new_product.format(
            **data["products"][-1]) + products + texts.CreateDocument.products_stats.format(summa=summa, count=count)
        await message.answer(msg_text, reply_markup=user_kb.product_menu)

    await CreateKP.product.set()
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(commands="correctuserdata")
@dp.message_handler(text="Изменить свои данные")
async def change_my_info(message: Message):
    user = db.get_user(message.from_user.id)
    if not user["is_activate"]:
        return

    await message.answer("Введите ФИ", reply_markup=user_kb.cancel)
    await message.delete()
    await ChangeMyInfo.fi.set()


@dp.message_handler(state=ChangeMyInfo.fi)
async def enter_fi(message: Message, state: FSMContext):
    await state.update_data(fi=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите должность: Менеджер отдела продаж")
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=ChangeMyInfo.role)
async def enter_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите e-mail")
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=ChangeMyInfo.email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите номер телефона")
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=ChangeMyInfo.number)
async def enter_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите номер офиса")
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=ChangeMyInfo.office_number)
async def enter_office_number(message: Message, state: FSMContext):
    await state.update_data(office_number=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите название сайта")
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=ChangeMyInfo.site)
async def enter_site(message: Message, state: FSMContext):
    await state.update_data(site=message.text)
    data = await state.get_data()
    db.change_my_info(data, message.from_user.id)

    await message.answer(f"""Ваши персональные данные обновлены:
ФИ {data['fi']}
Должность {data['role']}
E-mail {data['email']}
Номер телефона {data['number']}
Номер офиса {data['office_number']}
Название сайта {data['site']}""")
    await message.bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.delete()
    await state.finish()
