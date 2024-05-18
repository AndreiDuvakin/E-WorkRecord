import sys

from PyQt5.QtWidgets import QApplication
from json import loads, JSONDecodeError

from main_window import MainWindow

PATH_TO_DATA_FILE = 'data.json'


def check_data_file():
    try:
        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            loads(file.read())
    except Exception:
        with open(PATH_TO_DATA_FILE, 'w', encoding='utf-8') as file:
            file.write('[]')


def main():
    check_data_file()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
