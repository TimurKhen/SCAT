import random


def random_hex_value():
    hex_converted = hex(random.getrandbits(16))[2:].zfill(2)
    hex_converted2 = "{0:x}".format(round(random.random() * 100)).zfill(2)

    generated_hex = str(hex_converted[:1]) + str(hex_converted2[1:])

    return generated_hex


def generate_sum(n, count=256):
    random.seed(n)
    array = []

    for i in range(count):
        array.append(random_hex_value())

    return array
