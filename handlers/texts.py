admin_hello_text = "Вы вошли как администратор"
cancel_input = "Ввод остановлен"


class Provider:
    enter_name = "Введите название организации"
    enter_address = "Введите адрес"
    enter_inn = "Введите ИНН"
    enter_ogrn = "Введите ОГРН"
    enter_payment = "Введите расчетный счёт"
    enter_bank = "Введите банк"
    enter_correspondent = "Введите корреспондентский счёт"
    enter_bik = "Введите БИК"
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
{bank}
к/с {correspondent}
БИК {bik}
Тел.: {phone}
E-mail: {email}

Директор {director}

Обновляем поставщика?
"""
    finish = "Поставщик обновлен"
