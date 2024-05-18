from json import loads

from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QListWidget
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
        self.lineEdit.textChanged.connect(self.check_find_string)
        self.pushButton_2.clicked.connect(self.add_card)
        self.cards_info = []
        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            self.cards_info = loads(file.read())
        self.load_cards()

    def add_card(self):
        self.add_card_win = AddCardWin(self)
        self.add_card_win.show()
        self.close()

    def check_find_string(self):
        if self.lineEdit.text():
            self.pushButton.setVisible(True)
        else:
            self.pushButton.setVisible(False)

    def load_cards(self):
        self.listWidget.clear()
        for card in self.cards_info:
            card_widget = CardWidget()
            list_item = QListWidgetItem()
            card_widget.label.setText(
                f'{card["title"]["last_name"]} {card["title"]["first_name"]} - {card["title"]["issue_date"]}')
            card_widget.pushButton.card = card
            card_widget.pushButton.clicked.connect(self.open_card)
            list_item.setSizeHint(card_widget.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, card_widget)

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
