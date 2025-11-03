from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLabel

from interfaces.dataController import controller


class PasswordActions(QWidget):
    def __init__(self):
        super().__init__()
        if controller["key"] is None:
            errorLabel = QLabel("Please create an FlashCard first")
        else:
            uic.loadUi('ui/passwordActions_interface.ui', self)
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
            self.close()
        except Exception as e:
            print(e)
            self.label.setText('Неожиданная ошибка.')
