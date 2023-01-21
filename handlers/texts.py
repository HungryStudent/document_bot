hello = "Здравствуйте"
admin_hello_text = "Вы вошли как администратор"
cancel_input = "Ввод остановлен"
banks_menu = "Список банков"


class Provider:
    enter_name = "Введите название организации"
    enter_address = "Введите адрес"
    enter_inn = "Введите ИНН"
    enter_ogrn = "Введите ОГРН"
    enter_bank_id = "Выберите банк"
    enter_phone = "Введите телефон"
    enter_email = "Введите e-mail"
    enter_director = "Введите ФИО директора"
    check = """Поставщик: 
{name}
Юридический и почтовый адрес:
{address}
ИНН/КПП {inn}
ОГРН {ogrn}
р/с {payment}
{bank_name}
к/с {correspondent}
БИК {bik}
Тел.: {phone}
E-mail: {email}

Директор {director}

Обновляем поставщика?
"""
    finish = "Поставщик обновлен"


class Bank:
    enter_name = "Введите название банка"
    enter_bik = "Введите БИК"
    enter_correspondent = "Введите корреспондентский счёт"
    enter_payment = "Введите расчетный счёт"
    finish = "Банк добавлен"


class CreateDocument:
    enter_provider_bank = "Выберите банк поставщика"
    enter_org_type = "Выберите тип организации"
    enter_nds = "Выберите НДС"
    enter_number = "Введите номер договора"
    enter_inn = "Введите ИНН"
    enter_role = "Введите должность"
    enter_role_parent = "Введите должность в родительном падеже"
    enter_name = "Введите название организации"
    enter_kpp = "Введите КПП"
    enter_bank_name = "Введите название банка"
    enter_bik = "Введите БИК"
    enter_payment = "Введите расчетный счет"
    enter_correspondent = "Введите кор счет"
    enter_ogrn = "Введите ОГРН"
    enter_address = "Введите адрес"

    enter_fio = "Введите ФИО"
    enter_fio_parent = "Введите ФИО в родительном падеже"
    enter_phone = "Введите телефон"
    enter_email = "Введите почту"
    enter_product = "Добавление товаров в спецификацию контракта"
    new_product = """Добавлена спецификация
Наименование {name}
Количество {count}
Единицу измерения {type}
Цена за единицу {price}

"""
    product_info = "{name} {count}{type}цена:{price}\n"
    products_stats = """\nСумма: {summa}
Количество: {count}"""
    enter_name_product = "Укажите Наименование\nПример: Стопорная гайка"
    enter_count_product = "Укажите Количество\nПример: 13 или 1.55"
    enter_type_product = "Укажите Наименование\nПример: шт."
    enter_price_product = "Укажите Цену за единицу\nПример: 34.55"
    enter_doc_type = "Выберите тип документа"
    finish = "Документ создан"
    fio_error = "Введите корректное ФИО"
