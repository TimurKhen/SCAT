import random
import uuid

from SixteenNumbersGenerator import generator


def generate_headers():
    mac_num = uuid.getnode()
    mac_str = "{:012x}".format(mac_num)
    headers = ['ff', 'ff']

    for i in range(0, len(mac_str), 2):
        headers.append(mac_str[i] + mac_str[i + 1])
    return headers


def create_numeric_form(string):
    ords = 0
    for i in string:
        count_of_symbol = sum(map(int, str(ord(i))))

        ords += count_of_symbol

    return hex(ords)[2:].zfill(2)


def key_generator():
    count_of_keys = 0

    random.seed(None)
    codes = []

    codes.append("{:02x}".format(count_of_keys))
    count_of_keys += 1

    for j in range(256):
        codes.append(generator.random_hex_value())

    return codes


#
# v1 = generate_sum('1X#')
# h1 = generate_headers()
#
# with open('key.txt', 'w', encoding='utf-8') as f:
#     f.write(' '.join(v1) + '\n')
#     f.write(' '.join(h1) + '\n')
#
# save_key = create_numeric_form('1X#')
# print(save_key)
#
# k = generate_key('1X#')
#
# for i in range(255):
#     k = generate_key('1X#')
#     with open('key.txt', 'a', encoding='utf-8') as f:
#         f.write(' '.join(k) + '\n')
#
# create_hash('qwerty', k)

"""
v0 | h0 | body0 | body1 | body2 | body3 | body4 | body5

v0 - Тип строки
h0 - Доп значение - индекс
bodyN - ключ/адрес/контрольная сумма
"""

"""

"""
