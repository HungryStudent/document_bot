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


@dp.message_handler(text="Создать КП")
async def create_kp(message: Message):
    user = db.get_user(message.from_user.id)

    await message.answer("Введите номер коммерческого предложения")
    await CreateKP.number.set()

    """name = doc_gen.get_kp(user)

    if message.from_user.id in admin_ids:
        kb = admin_kb.menu
    else:
        kb = user_kb.menu

    await message.answer_document(open(name + ".docx", "rb"), caption="КП",
                                  reply_markup=kb)"""


@dp.message_handler(state=CreateKP.number)
async def kp_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await CreateKP.next()
    await message.answer("Выберите НДС", reply_markup=user_kb.nds)


@dp.callback_query_handler(state=CreateKP.nds)
async def kp_nds(call: CallbackQuery, state: FSMContext):
    await state.update_data(nds=int(call.data.split(":")[1]))
    await state.update_data(products=[])
    await CreateKP.next()
    await call.message.answer("Добавление товаров в спецификацию", reply_markup=user_kb.add_product)
    await call.answer()


@dp.callback_query_handler(state=CreateKP.product)
async def kp_product(call: CallbackQuery, state: FSMContext):
    if call.data == "finish_product":
        document_data = await state.get_data()
        user = db.get_user(call.from_user.id)
        document_data = {**document_data, **user}
        document_data["tbl_contents"] = document_data["products"]
        kp_name = doc_gen.get_kp(document_data)

        if call.from_user.id in admin_ids:
            kb = admin_kb.menu
        else:
            kb = user_kb.menu
        await call.message.answer_document(open(kp_name + ".docx", "rb"), caption="Документ создан",
                                           reply_markup=kb)
        await state.finish()
        await call.answer()
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
                                 "price": round(data["price_product"], 2),
                                 "cost": round(data["count_product"] * data["price_product"], 2)})
        products = ""
        summa = 0
        for product in data["products"]:
            products += "{name} {count}{type}цена:{price}\n".format(**product)
            summa += product["cost"]

        if float(summa).is_integer():
            data["summa"] = int(summa)
            data["rubles"] = int(summa)
            data["cents"] = "00"
            data["cents_text"] = "00 копеек"
        else:
            data["summa"] = format(round(summa, 2), '.2f')
            data["rubles"] = int(float(data["summa"]))

            data["cents"] = str(data["summa"])[-2:]
            data["cents_text"] = str(data["cents"]) + " " + text_funcs.get_text_variant(int(str(data["summa"])[-2:]),
                                                                                        "копейка, копейки, копеек")
        data["rubles_text"] = str(data["rubles"]) + " " + text_funcs.get_text_variant(int(float(data["summa"])),
                                                                                      "рубль, рубля, рублей")
        data["string_summa_text"] = get_string_by_number(summa)
        data["summa_text"] = f'{data["rubles_text"]} {data["cents_text"]} ({data["string_summa_text"]})'
        nds_summa = summa * data["nds"] * 0.01

        if float(nds_summa).is_integer():
            data["nds_summa"] = int(nds_summa)
            data["nds_rubles"] = int(nds_summa)
            data["nds_cents"] = "00"
            data["nds_cents_text"] = "00 копеек"
        else:
            data["nds_summa"] = format(round(nds_summa, 2), '.2f')
            data["nds_rubles"] = int(float(data["nds_summa"]))
            data["nds_cents"] = str(data["nds_summa"])[-2:]
            data["nds_cents_text"] = str(data["nds_cents"]) + " " + text_funcs.get_text_variant(
                int(str(data["nds_summa"])[-2:]),
                "копейка, копейки, копеек")

        data["nds_rubles_text"] = str(data["nds_rubles"]) + " " + text_funcs.get_text_variant(
            int(float(data["nds_summa"])),
            "рубль, рубля, рублей")
        data["nds_summa_text"] = f'{data["nds_rubles_text"]} {data["nds_cents_text"]}'
        count = len(data["products"])
        data["products_count"] = count
        msg_text = texts.CreateDocument.new_product.format(
            **data["products"][-1]) + products + texts.CreateDocument.products_stats.format(summa=summa, count=count)
        await message.answer(msg_text, reply_markup=user_kb.product_menu)

    await CreateKP.product.set()
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(text="Изменить свои данные")
async def change_my_info(message: Message):
    await message.answer("Введите ФИ", reply_markup=user_kb.cancel)
    await ChangeMyInfo.fi.set()


@dp.message_handler(state=ChangeMyInfo.fi)
async def enter_fi(message: Message, state: FSMContext):
    await state.update_data(fi=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите должность")


@dp.message_handler(state=ChangeMyInfo.role)
async def enter_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите e-mail")


@dp.message_handler(state=ChangeMyInfo.email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите номер телефона")


@dp.message_handler(state=ChangeMyInfo.number)
async def enter_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите номер офиса")


@dp.message_handler(state=ChangeMyInfo.office_number)
async def enter_office_number(message: Message, state: FSMContext):
    await state.update_data(office_number=message.text)
    await ChangeMyInfo.next()
    await message.answer("Введите название сайта")


@dp.message_handler(state=ChangeMyInfo.site)
async def enter_site(message: Message, state: FSMContext):
    await state.update_data(site=message.text)
    data = await state.get_data()
    db.change_my_info(data, message.from_user.id)

    if message.from_user.id in admin_ids:
        kb = admin_kb.menu
    else:
        kb = user_kb.menu

    await message.answer(f"""Ваши персональные данные обновлены:
ФИ {data['fi']}
Должность {data['role']}
E-mail {data['email']}
Номер телефона {data['number']}
Номер офиса {data['office_number']}
Название сайта {data['site']}""", reply_markup=kb)
    await state.finish()
