import os

from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QWidget

from interfaces.dataController import controller
from interfaces.flashCardMethods.key import Key
from interfaces.resource import resource_path


class CreateNewFlashCard(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('ui/createNewFlash_interface.ui'), self)
        # self.folder_path = folder_path
        self.initUI()

    def initUI(self):
        self.chooseFlash.clicked.connect(self.select_folder)
        self.sureCheckBox.stateChanged.connect(self.changed_status_of_sure)
        self.createFlash.setEnabled(False)
        self.createFlash.clicked.connect(self.create_flash)
        self.controlText.setMaxLength(3)
        self.controlText.textChanged.connect(self.changed_status_of_sure)

    def select_folder(self):
        directory = QFileDialog.getExistingDirectory(self)
        self.selectedFlashName.setText(str(directory))
        self.flash_card_for = directory

    def changed_status_of_sure(self):
        self.createFlash.setEnabled(self.sureCheckBox.isChecked() and len(self.controlText.text()) == 3)

    def passwords_file_cleaner(self):
        try:
            password_path = "C://SCAT/passwords.txt"

            password_path = os.path.normpath(password_path)

            directory = os.path.dirname(password_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(password_path, 'w') as f:
                f.write('')

            print(f"Файл {password_path} успешно очищен")

        except Exception as e:
            print(e)

    def create_flash(self):
        if self.flash_card_for is None:
            return
        self.passwords_file_cleaner()

        try:
            key = Key(self.flash_card_for)
            controller["key"] = key
            controller["flash_card_path"] = self.flash_card_for

            path = [
                {
                    'worker': key,
                    'status': 'Создание ключей'
                }
            ]

            try:
                for i in path:
                    i['worker'].run()
                    self.selectedFlashName.setText(str(i['status']))

                self.selectedFlashName.setText('Флешкарта успешно создана')
            except Exception as e:
                self.selectedFlashName.setText(f'Ошибка во время создания флешкарты: {e}')
                print(e)
        except Exception as e:
            print(e)
