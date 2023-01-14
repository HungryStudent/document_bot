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