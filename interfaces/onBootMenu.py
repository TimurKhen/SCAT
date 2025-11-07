from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QFileDialog

from interfaces.dataController import controller


class GetInformationOfFlashCard(QWidget):
    flash_card_selected = pyqtSignal(str)
    flash_card_created = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/FlashCardOnOpen_interface.ui', self)
        self.setGeometry(400, 300, 400, 300)
        self.initUI()

    def initUI(self):
        self.connectFlashCard_2.clicked.connect(self.select_flash)
        self.createFlashCard.clicked.connect(self.create_flash)

    def select_flash(self):
        directory = QFileDialog.getExistingDirectory(self)
        if directory:
            controller["flash_card_path"] = directory
            self.flash_card_selected.emit(directory)
            self.close()

    def create_flash(self):
        self.flash_card_created.emit('')
        self.close()
