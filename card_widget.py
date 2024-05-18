from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class CardWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/JobCard.ui', self)
