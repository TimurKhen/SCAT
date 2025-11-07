import ctypes
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget

from interfaces.createNewFlashCard import CreateNewFlashCard
from interfaces.dataController import controller
from interfaces.flashCardMethods.key import Key
from interfaces.onBootMenu import GetInformationOfFlashCard
from interfaces.passwordsActions import PasswordActions


class Scat(QMainWindow):
    def __init__(self):
        super().__init__()
        if not self.is_admin():
            self.restart_as_admin()
        else:
            uic.loadUi('ui/main_interface.ui', self)
            self.passwords_in_layout = []
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
        # self.actionChange_current_flash_keys.triggered.connect(self.change_current_flash_card)
        self.actionAdd_password.triggered.connect(self.add_password)
        # self.actionRemove_password.triggered.connect(self.clear_password)

        self.setup_scroll_area()

        self.password_setter()

    def setup_scroll_area(self):
        """Настройка скроллируемой области для паролей"""
        # Создаем виджет-контейнер для кнопок
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(2)  # Небольшой отступ между кнопками

        # Создаем область прокрутки
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.scroll_widget)

        # Добавляем scroll area в существующий passwordsLayout
        self.passwordsLayout.addWidget(self.scroll_area)

    def create_new_flash_card(self):
        self.create_new_flash_card_form = CreateNewFlashCard()
        self.create_new_flash_card_form.show()
        print('Created new flash card')

    def add_password(self):
        self.add_new_password_form = PasswordActions(self.passwords_in_layout[-1])
        self.add_new_password_form.password_add.connect(self.load_passwords)
        self.add_new_password_form.show()
        print('Adding new password')

    def password_setter(self):
        self.bootMenu = GetInformationOfFlashCard()
        self.bootMenu.flash_card_selected.connect(self.on_flash_card_selected)
        self.bootMenu.flash_card_created.connect(self.create_new_flash_card)
        self.bootMenu.show()

    def get_last_key_index(self):
        with open(f'{controller["flash_card_path"]}/key.txt', 'r', encoding='utf-8') as f:
            readed = f.read()
            data = readed.split('\n')
            return len(data) - 1

    def on_flash_card_selected(self, directory_path):
        key = Key(directory_path, self.get_last_key_index())
        controller["key"] = key
        self.load_passwords()
        print(controller)

    def load_passwords(self):
        try:
            if controller.get('flash_card_path'):
                password_path = "C:\Program Files\SCAT\passwords.txt"
                with open(password_path, "r") as f:
                    line = f.readline()

                    while line:
                        line = line.strip()
                        if not line:
                            line = f.readline()
                            continue

                        splited = line.split(" ")
                        if len(splited) >= 9 and int(splited[2]) in self.passwords_in_layout:
                            line = f.readline()
                            continue

                        if len(splited) >= 9:
                            button = QPushButton(f'{splited[2]}: {splited[8]}')
                            button.setFixedHeight(30)
                            button.setStyleSheet("""
                                QPushButton {
                                    text-align: left;
                                    padding: 5px;
                                }
                                QPushButton:hover {
                                    background-color: #e0e0e0;
                                }
                            """)
                            self.scroll_layout.addWidget(button)
                            self.passwords_in_layout.append(int(splited[2]))

                        line = f.readline()

        except FileExistsError and FileNotFoundError:
            password_path = "C:\Program Files\SCAT\passwords.txt"
            with open(password_path, "w") as f:
                f.write("")
        except Exception as e:
            print(e, "maybe file doesn't exist or user need to create passwords")

    def clear_passwords_layout(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.passwords_in_layout.clear()
