import os

from PyQt6 import uic
from PyQt6.QtWidgets import QFileDialog, QWidget

from interfaces.dataController import controller
from interfaces.flashCardMethods.key import Key


class CreateNewFlashCard(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/createNewFlash_interface.ui', self)
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
        password_path = "C:\Program Files\SCAT\passwords.txt"
        with open(password_path, 'w') as f:
            pass

    def create_flash(self):
        if not self.flash_card_for:
            return
        self.passwords_file_cleaner()

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

        # self.close()
