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
    enter_number = "Введите номер договора\nПример: 123123 или 123-123"
    enter_inn = "Введите ИНН\nПример: 123456789"
    enter_role = "Введите должность\nПример: Генеральный директор"
    enter_role_parent = "Введите должность в родительном падеже\nПример: Генерального директора"
    enter_name = "Введите название организации\nПример: ООО «Альбатрос»"
    enter_kpp = "Введите КПП\nПример: 123456789"
    enter_bank_name = "Введите название банка\nПример: Тинькофф Банк"
    enter_bik = "Введите БИК\nПример: 123456789"
    enter_payment = "Введите расчетный счет\nПример: 123456789 или 12345-6789"
    enter_correspondent = "Введите кор счет\nПример: 123456789"
    enter_ogrn = "Введите ОГРН\nПример: 123456789"
    enter_address = "Введите адрес\nПример: 159050, г. Санкт-Петербург, Новый тупик, д.23, стр.4"

    enter_fio = "Введите ФИО\nПример: Иванов Владимир Владимирович"
    enter_fio_parent = "Введите ФИО в родительном падеже\nПример: Иванова Владимира Владимировича"
    enter_phone = "Введите телефон\nПример: +7(900)001-01-01"
    enter_email = "Введите почту\nПример: 123@gmail.com"
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
