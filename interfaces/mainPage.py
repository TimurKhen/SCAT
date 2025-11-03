import ctypes
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QPushButton

from interfaces.createNewFlashCard import CreateNewFlashCard
from interfaces.passwordsActions import PasswordActions


class Scat(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        if not self.is_admin():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Требуются права администратора")
            msg.setText("SCAT требует права администратора для работы")
            msg.setInformativeText("Хотите перезапустить приложение с правами администратора?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if msg.exec() == QMessageBox.StandardButton.Yes:
                self.restart_as_admin()
            else:
                self.close()
        else:
            uic.loadUi('ui/main_interface.ui', self)
            self.initUI()

    def restart_as_admin(self):
        if sys.platform.startswith('win'):
            script = sys.argv[0]
            params = ' '.join([f'"{x}"' for x in sys.argv[1:]])
            try:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script}" {params}', None, 1
                )
                sys.exit(0)
            except Exception as e:
                print(e)
        return False

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def initUI(self):
        self.menu_bar = self.menuBar()
        self.actionCreate_new_flash_key.triggered.connect(self.create_new_flash_card)
        self.actionChange_current_flash_keys.triggered.connect(self.change_current_flash_card)
        self.actionAdd_password.triggered.connect(self.add_password)
        self.actionRemove_password.triggered.connect(self.clear_password)
        self.password_setter()

    def create_new_flash_card(self):
        self.create_new_flash_card_form = CreateNewFlashCard()
        self.create_new_flash_card_form.show()
        print('Created new flash card')

    def change_current_flash_card(self):
        print('Changed current flash card')

    def add_password(self):
        self.add_new_password_form = PasswordActions()
        self.add_new_password_form.show()
        print('Adding new password')

    def clear_password(self):
        print('Clearing password')

    def password_setter(self):
        import os

        try:
            password_path = r"C:\Program Files\SCAT\passwords.txt"
            target_dir = os.path.dirname(password_path)
            os.makedirs(target_dir, exist_ok=True)

            with open(password_path, "r") as f:
                # password_file.write('')
                line = f.readline()
                while line:
                    line = line.strip()

                    splited = line.split(" ")

                    button = QPushButton(f'{splited[2]}: {splited[8]}')
                    self.passwordsLayout.addWidget(button)

                    line = f.readline()
        except Exception as e:
            print(e, "maybe file doesn't exist")
