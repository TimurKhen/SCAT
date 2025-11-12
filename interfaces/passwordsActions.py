from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel

from interfaces.dataController import controller
from interfaces.resource import resource_path


class PasswordActions(QWidget):
    password_add = pyqtSignal(str)

    def __init__(self, last_password_index=0):
        super().__init__()
        if controller["key"] is None:
            self.errorLabel = QLabel("Please create an FlashCard first")
        else:
            uic.loadUi(resource_path('ui/passwordActions_interface.ui'), self)
            self.last_password_index = last_password_index
            self.initUI()

    def initUI(self):
        self.clearButton.clicked.connect(self.clear_event)
        self.addButton.clicked.connect(self.add_event)
        self.pushButton.clicked.connect(self.open_url)

    def open_url(self):
        try:
            url = QUrl('https://github.com/TimurKhen/X256/blob/master/README.md')
            QDesktopServices.openUrl(url)
        except Exception as e:
            print(e)

    def clear_event(self):
        self.passwordLine.setText("")
        self.usernameLine.setText("")
        self.serviceLine.setText("")

    def add_event(self):
        try:
            username = str(self.usernameLine.text())
            password = str(self.passwordLine.text())
            service = str(self.serviceLine.text())
            controller["key"].add_password(username, password, service)
            self.password_add.emit('')
            self.close()
        except Exception as e:
            print(e)
            self.label.setText('Неожиданная ошибка.')
