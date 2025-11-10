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
    random.seed(None)
    codes = []

    for j in range(256):
        codes.append(generator.random_hex_value())

    return codes