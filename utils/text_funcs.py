def get_text_variant(amount, variants):
    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif 2 <= amount % 10 <= 4 and \
            (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants.split(", ")[variant]