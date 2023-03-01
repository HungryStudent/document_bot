from number_to_string import get_string_by_number

data = {}
summa = 12.01


def get_text_variant(amount, variants):
    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif amount % 10 >= 2 and amount % 10 <= 4 and \
            (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants.split(", ")[variant]


nds_summa = 12.01
if float(nds_summa).is_integer():
    data["nds_summa"] = int(nds_summa)
    data["nds_rubles"] = int(nds_summa)
    data["nds_cents"] = "00"
    data["nds_cents_text"] = "00 копеек"
else:
    data["nds_summa"] = format(round(nds_summa, 2), '.2f')
    data["nds_rubles"] = int(float(data["nds_summa"]))
    data["nds_cents"] = str(data["nds_summa"])[-2:]
    data["nds_cents_text"] = str(data["nds_cents"]) + " " + get_text_variant(int(str(data["nds_summa"])[-2:]),
                                                                             "копейка, копейки, копеек")

data["nds_rubles_text"] = str(data["nds_rubles"]) + " " + get_text_variant(int(float(data["nds_summa"])),
                                                                           "рубль, рубля, рублей")
data["nds_summa_text"] = f'{data["nds_rubles_text"]} {data["nds_cents_text"]}'

print(data)
