import datetime
import os
from json import loads, dumps

from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QListWidget, QMessageBox, QFileDialog
from PyQt5 import uic

from add_card_window import AddCardWin
from card_widget import CardWidget
from view_card_window import ViewCardWin

PATH_TO_DATA_FILE = 'data.json'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/MainWin.ui', self)
        self.pushButton.setVisible(False)
        self.pushButton.clicked.connect(self.clear_find)
        self.lineEdit.textChanged.connect(self.check_find_string)
        self.pushButton_2.clicked.connect(self.add_card)
        self.pushButton_3.clicked.connect(self.dump_checked)
        self.checkBox.stateChanged.connect(self.select_all)
        self.cards_info = []
        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            self.cards_info = loads(file.read())
        self.checked_cards = []
        self.load_cards()

    def select_all(self):
        for item_index in range(self.listWidget.count()):
            item = self.listWidget.item(item_index)
            widget = self.listWidget.itemWidget(item)
            widget.checkBox.blockSignals(True)
            widget.checkBox.setChecked(self.checkBox.isChecked())
            widget.checkBox.blockSignals(False)

    def dump_checked(self):
        if not self.checked_cards:
            QMessageBox.warning(self, 'Ошибка выгрузки данных', 'Не выбраны книжки для выгрузки')
            return

        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Выберите путь сохранения", options=options)

        if directory:
            dumping_card_info = []
            for card in self.checked_cards:
                copy_card = card.copy()
                del copy_card['uuid']
                dumping_card_info.append(copy_card)

            file_name = os.path.join(directory,
                                     f'Трудовые книжки - {str(datetime.date.today())}.json')
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(dumps(dumping_card_info))

            QMessageBox.information(self, 'Данные выгружены', 'Данные успешно выгружены в файл')

    def clear_find(self):
        self.lineEdit.clear()

    def add_card(self):
        self.add_card_win = AddCardWin(self)
        self.add_card_win.show()
        self.close()

    def check_find_string(self):
        if self.lineEdit.text():
            self.pushButton.setVisible(True)
        else:
            self.pushButton.setVisible(False)

        self.find_card()

    def find_card(self):
        for item_index in range(self.listWidget.count()):
            item = self.listWidget.item(item_index)
            widget = self.listWidget.itemWidget(item)
            if self.lineEdit.text().lower().strip() in widget.label.text().lower().strip():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def load_cards(self):
        self.listWidget.clear()
        for card in self.cards_info:
            card_widget = CardWidget()
            list_item = QListWidgetItem()
            card_widget.label.setText(
                f'{card["title"]["last_name"]} {card["title"]["first_name"]} - {card["title"]["issue_date"]}')
            card_widget.checkBox.stateChanged.connect(self.select_card)
            card_widget.checkBox.card = card
            card_widget.pushButton.card = card
            card_widget.pushButton.clicked.connect(self.open_card)
            list_item.setSizeHint(card_widget.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, card_widget)

    def select_card(self):
        sender = self.sender()
        if sender.isChecked():
            self.checked_cards.append(sender.card.copy())
        else:
            del self.checked_cards[self.checked_cards.index(sender.card)]
        self.checkBox.blockSignals(True)
        self.checkBox.setChecked(len(self.checked_cards) == len(self.cards_info))
        self.checkBox.blockSignals(False)

    def open_card(self):
        sender = self.sender()
        self.view_card = ViewCardWin(self, sender.card)
        self.view_card.show()
        self.close()

    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            self.cards_info = loads(file.read())
        self.load_cards()
