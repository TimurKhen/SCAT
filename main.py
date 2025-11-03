import sys

from PyQt6.QtWidgets import QApplication

from interfaces.mainPage import Scat

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Scat()
    ex.show()
    sys.exit(app.exec())
