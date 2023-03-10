from enum import Enum

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import keyboards.admin as admin_kb
import keyboards.user as user_kb
from config import admin_ids
from create_bot import dp
from handlers import texts
from states import user as states
from utils import db
from utils import doc_gen

from number_to_string import get_string_by_number

from utils import text_funcs


class DocTypes(Enum):
    docx = 1
    pdf = 2


@dp.message_handler(commands='start', state="*")
async def start_message(message: Message, state: FSMContext):
    await state.finish()
    user = db.get_user(message.from_user.id)
    if user is None:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    if message.from_user.id in admin_ids:
        await message.answer(texts.admin_hello_text, reply_markup=admin_kb.menu)
    else:
        await message.answer(texts.hello, reply_markup=user_kb.menu)


@dp.message_handler(text="Создать договор")
async def start_create_document(message: Message):
    await states.CreateDocument.enter_provider_bank.set()
    await message.answer("Начинаем создание", reply_markup=user_kb.cancel)
    await message.answer(texts.CreateDocument.enter_provider_bank, reply_markup=user_kb.get_banks())


@dp.message_handler(state="*", text="Отмена")
async def cancel_user(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.cancel_input, reply_markup=user_kb.menu)


@dp.callback_query_handler(user_kb.bank_data.filter(), state=states.CreateDocument.enter_provider_bank)
async def enter_provider_bank(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(provider_bank=callback_data["id"])

    await states.CreateDocument.next()
    await call.message.answer(texts.CreateDocument.enter_org_type, reply_markup=user_kb.org_type)
    await call.bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    await call.message.delete()
    await call.answer()


@dp.callback_query_handler(state=states.CreateDocument.enter_org_type)
async def enter_org_type(call: CallbackQuery, state: FSMContext):
    await state.update_data(org_type=call.data.split(":")[1])

    await states.CreateDocument.next()
    await call.message.answer(texts.CreateDocument.enter_nds, reply_markup=user_kb.nds)
    await call.message.delete()
    await call.answer()


@dp.callback_query_handler(state=states.CreateDocument.enter_nds)
async def enter_nds(call: CallbackQuery, state: FSMContext):
    await state.update_data(nds=int(call.data.split(":")[1]))

    await states.CreateDocument.next()
    await call.message.answer(texts.CreateDocument.enter_number)
    await call.message.delete()
    await call.answer()


@dp.message_handler(state=states.CreateDocument.enter_number)
async def enter_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_inn)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_inn)
async def enter_inn(message: Message, state: FSMContext):
    await state.update_data(inn=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_role)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_role)
async def enter_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_role_parent)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_role_parent)
async def enter_role_parent(message: Message, state: FSMContext):
    await state.update_data(role_parent=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_name)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_kpp)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_kpp)
async def v(message: Message, state: FSMContext):
    await state.update_data(kpp=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_bank_name)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_bank_name)
async def enter_bank_name(message: Message, state: FSMContext):
    await state.update_data(bank_name=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_bik)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_bik)
async def enter_bik(message: Message, state: FSMContext):
    await state.update_data(bik=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_payment)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_payment)
async def enter_payment(message: Message, state: FSMContext):
    await state.update_data(payment=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_correspondent)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_correspondent)
async def enter_correspondent(message: Message, state: FSMContext):
    await state.update_data(correspondent=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_ogrn)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_ogrn)
async def enter_ogrn(message: Message, state: FSMContext):
    await state.update_data(ogrn=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_address)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_address)
async def enter_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_fio)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_fio)
async def enter_fio(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 3:
        await message.answer(texts.CreateDocument.fio_error)
        return
    await state.update_data(fio=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_fio_parent)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_fio_parent)
async def enter_fio_parent(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 3:
        await message.answer(texts.CreateDocument.fio_error)
        return
    await state.update_data(fio_parent=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_phone)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(enter_phone=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_email)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.update_data(products=[])
    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_product, reply_markup=user_kb.add_product)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.callback_query_handler(state=states.CreateDocument.enter_product)
async def enter_product(call: CallbackQuery, state: FSMContext):
    if call.data == "finish_product":
        document_data = await state.get_data()
        document_data = {**document_data, **db.get_bank(document_data["provider_bank"])}
        document_data[
            "fio_iniz"] = f'{document_data["fio"].split(" ")[0]} {document_data["fio"].split(" ")[1][0]}.{document_data["fio"].split(" ")[2][0]}.'
        document_data["tbl_contents"] = document_data["products"]
        document_data["short_name"] = document_data["name"].replace("ООО ", "")
        doc_name, bill_name = doc_gen.get_docx(document_data)

        if call.from_user.id in admin_ids:
            kb = admin_kb.menu
        else:
            kb = user_kb.menu
        await call.message.answer_document(open(doc_name + ".docx", "rb"), caption=texts.CreateDocument.finish,
                                           reply_markup=kb)
        await call.message.answer_document(open(bill_name + ".docx", "rb"), caption=texts.CreateDocument.finish)
        await call.message.answer_document(open(doc_name + ".pdf", "rb"), caption=texts.CreateDocument.finish)
        await call.message.answer_document(open(bill_name + ".pdf", "rb"), caption=texts.CreateDocument.finish)
        # await call.message.delete()
        await state.finish()
        await call.answer()
        return

    await states.CreateDocument.next()
    await call.message.answer(texts.CreateDocument.enter_name_product)
    await call.message.delete()
    await call.answer()


@dp.message_handler(state=states.CreateDocument.enter_name_product)
async def enter_name_product(message: Message, state: FSMContext):
    await state.update_data(name_product=message.text)

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_count_product)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.message_handler(state=states.CreateDocument.enter_count_product)
async def enter_count_product(message: Message, state: FSMContext):
    count_product = message.text.replace(",", ".")
    try:
        await state.update_data(count_product=float(count_product))
    except ValueError:
        await message.answer("Введите число!")
        return

    await states.CreateDocument.next()
    await message.answer(texts.CreateDocument.enter_type_product, reply_markup=user_kb.type_product)
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()


@dp.callback_query_handler(Text(startswith="type_product"), state=states.CreateDocument.enter_type_product)
async def enter_type_product(call: CallbackQuery, state: FSMContext):
    await state.update_data(type_product=int(call.data.split(":")[1]))

    await states.CreateDocument.next()
    await call.message.answer(texts.CreateDocument.enter_price_product)
    await call.message.delete()
    await call.answer()


@dp.message_handler(state=states.CreateDocument.enter_price_product)
async def enter_price_product(message: Message, state: FSMContext):
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
            products += texts.CreateDocument.product_info.format(**product)
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

    await states.CreateDocument.enter_product.set()
    await message.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
