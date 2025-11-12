import ctypes
import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget

from interfaces.createNewFlashCard import CreateNewFlashCard
from interfaces.dataController import controller
from interfaces.flashCardMethods.key import Key
from interfaces.onBootMenu import GetInformationOfFlashCard
from interfaces.passwordShower import PasswordShower
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
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(2)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.scroll_widget)

        self.passwordsLayout.addWidget(self.scroll_area)

    def on_flash_card_selected(self, directory_path):
        flash_path = controller["flash_card_path"]

        if flash_path is not None:
            key = Key(directory_path, self.get_last_key_index())
            controller["key"] = key
            self.load_passwords()

    def create_new_flash_card(self):
        self.create_new_flash_card_form = CreateNewFlashCard()
        self.create_new_flash_card_form.show()

    def get_last_key_index(self):
        flash_path = controller["flash_card_path"]
        with open(f'{flash_path}/key.txt', 'r', encoding='utf-8') as f:
            readed = f.read()
            data = readed.split('\n')
            return len(data) - 1

    def add_password(self):
        if controller["flash_card_path"]:
            self.add_new_password_form = PasswordActions(self.get_last_key_index())
            self.add_new_password_form.password_add.connect(self.load_passwords)
            self.add_new_password_form.show()

    def password_setter(self):
        self.bootMenu = GetInformationOfFlashCard()
        self.bootMenu.flash_card_selected.connect(self.on_flash_card_selected)
        self.bootMenu.flash_card_created.connect(self.create_new_flash_card)
        self.bootMenu.show()

    def password_create_form(self):
        username_from_sender = self.sender().property("username")
        password_from_sender = self.sender().property("password")
        service_from_sender = self.sender().property("service")
        index = self.sender().property("index")

        data = [username_from_sender, password_from_sender, service_from_sender]
        self.password_form = PasswordShower(index, data)
        self.password_form.show()

    def load_passwords(self):
        try:
            if controller.get('flash_card_path'):
                password_path = "C://SCAT/passwords.txt"
                print(os.path.exists(password_path))
                if not os.path.exists(password_path):
                    with open(password_path, "w") as f:
                        f.write("")

                with open(password_path, "r") as f:
                    line = f.readline()

                    while line:
                        line = line.strip()
                        if not line:
                            line = f.readline()
                            continue

                        splited = line.split(" ")
                        if int(splited[1]) in self.passwords_in_layout:
                            line = f.readline()
                            continue

                        if len(splited) >= 4:
                            button = QPushButton(f'{splited[1]}: {splited[3]}')
                            button.setFixedHeight(30)
                            button.setStyleSheet("""
                                QPushButton {
                                    text-align: left;
                                    padding: 5px;
                                }
                                QPushButton:hover {
                                    background-color: #88706B;
                                }
                            """)
                            button.clicked.connect(self.password_create_form)
                            button.setProperty("password", splited[0])
                            button.setProperty("username", splited[2])
                            button.setProperty("service", splited[3])
                            button.setProperty("index", splited[1])

                            self.scroll_layout.addWidget(button)
                            self.passwords_in_layout.append(int(splited[1]))

                        line = f.readline()

        except FileExistsError and FileNotFoundError:
            password_path = "C://SCAT/passwords.txt"
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
