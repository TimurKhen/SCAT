import math
import random

import pyperclip
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from X256.X256 import X256
from interfaces.dataController import controller


class PasswordShower(QWidget):
    def __init__(self, index, data):
        super().__init__()
        self.index = int(index)
        self.username = data[0]
        self.coded_password = data[1]
        self.service = data[2]

        uic.loadUi('ui/read_password.ui', self)
        self.initUI()

    def initUI(self):
        # self.close_button.clicked.connect(self.close)

        self.username_label.setText(self.username)
        self.password_label.setText(self.show_by_stars())
        self.service_label.setText(self.service)
        self.show_password_button.clicked.connect(self.show_password)
        self.close_button.clicked.connect(self.close)

    def get_key_by_index(self):
        with open(f'{controller["flash_card_path"]}/key.txt', 'r', encoding='utf-8') as f:
            readed = f.read()
            data = readed.split('\n')
            return data[self.index].split(' ')[1:]

    def show_by_stars(self):
        stars_handler = '*' * (5 + math.floor(random.randint(-3, 3)))
        return stars_handler

    def show_password(self):
        B = X256()
        key = self.get_key_by_index()
        decoded_value = B.decode(self.coded_password, key)
        self.password_label.setText('Copied!')
        pyperclip.copy(decoded_value)
