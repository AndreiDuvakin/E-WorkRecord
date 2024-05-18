import datetime
import uuid
from json import loads, dumps

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QSpinBox, QDateEdit, QPushButton, QTableWidgetItem

from view_card_window import ViewCardWin

PATH_TO_DATA_FILE = 'data.json'


class AddCardWin(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('ui/AddCardWin.ui', self)
        self.par = parent
        self.pushButton.clicked.connect(self.back)
        self.dateEdit_2.setDate(datetime.date.today())
        self.pushButton_2.clicked.connect(self.lets_scan)
        self.pushButton_3.clicked.connect(self.save_data)
        self.pushButton_4.clicked.connect(self.add_row)
        self.tableWidget.verticalHeader().setVisible(False)
        QTimer.singleShot(100, self.resize_table)

    def delete_row(self):
        sender = self.sender()
        self.tableWidget.removeRow(sender.row)

        for row in range(sender.row, self.tableWidget.rowCount()):
            self.tableWidget.cellWidget(row, 4).row -= 1

    def add_row(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

        number_spin_box = QSpinBox(self)
        number_spin_box.setMinimum(1)
        number_spin_box.setMaximum(100000)
        number_spin_box.setValue(self.tableWidget.rowCount())
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, number_spin_box)

        date_edit = QDateEdit()
        date_edit.setDate(datetime.date.today())
        date_edit.setMaximumDate(datetime.date.today())
        date_edit.setCalendarPopup(True)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 1, date_edit)

        delete_button = QPushButton()
        delete_button.setText('Удалить')
        delete_button.row = self.tableWidget.rowCount() - 1
        delete_button.clicked.connect(self.delete_row)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 4, delete_button)

        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(''))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(''))

        self.resize_table()

    def resize_table(self):
        if self.tableWidget.rowCount():
            row_height = min([90, max([50, self.tableWidget.height() // self.tableWidget.rowCount()])])

            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHeight(row, row_height)

        column_width = max([100, self.tableWidget.width() // self.tableWidget.columnCount()])

        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(column, column_width)

    def resizeEvent(self, a0, QResizeEvent=None):
        self.resize_table()

    def save_data(self):
        card_info = {
            "uuid": str(uuid.uuid4()),
            "title": {
                "serial": self.lineEdit.text(),
                "number": self.lineEdit_2.text(),
                "first_name": self.lineEdit_4.text(),
                "last_name": self.lineEdit_3.text(),
                "patronymic": self.lineEdit_5.text(),
                "birthday": str(self.dateEdit.date().toPyDate()),
                "issue_date": str(self.dateEdit_2.date().toPyDate()),
                "profession": self.lineEdit_6.text(),
                "education": self.lineEdit_7.text()
            },
            "job": [
                {
                    "number": self.tableWidget.cellWidget(row, 0).value(),
                    "date": str(self.tableWidget.cellWidget(row, 1).date().toPyDate()),
                    "job_info": self.tableWidget.item(row, 2).text(),
                    "basis": self.tableWidget.item(row, 3).text()
                }
                for row in range(self.tableWidget.rowCount())
            ]
        }

        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            data = loads(file.read())

        data.append(card_info)

        with open(PATH_TO_DATA_FILE, 'w', encoding='utf-8') as write_file:
            write_file.write(dumps(data))

        self.view_win = ViewCardWin(self.par, card_info)
        self.view_win.show()
        self.close()

    def lets_scan(self):
        pass

    def back(self):
        self.par.show()
        self.close()
