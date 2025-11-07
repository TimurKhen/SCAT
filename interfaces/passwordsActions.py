from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel

from interfaces.dataController import controller


class PasswordActions(QWidget):
    password_add = pyqtSignal(str)

    def __init__(self, last_password_index=0):
        super().__init__()
        if controller["key"] is None:
            self.errorLabel = QLabel("Please create an FlashCard first")
        else:
            uic.loadUi('ui/passwordActions_interface.ui', self)
            self.last_password_index = last_password_index
            self.initUI()

    def initUI(self):
        self.clearButton.clicked.connect(self.clear_event)
        self.addButton.clicked.connect(self.add_event)

    def clear_event(self):
        self.passwordLine.setText("")
        self.usernameLine.setText("")
        self.serviceLine.setText("")

    def add_event(self):
        try:
            password = self.passwordLine.text()
            username = self.usernameLine.text()
            service = self.serviceLine.text()
            controller["key"].add_password(username, password, service)
            self.password_add.emit('')
            self.close()
        except Exception as e:
            print(e)
            self.label.setText('Неожиданная ошибка.')
