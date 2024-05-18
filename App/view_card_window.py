import datetime
import os
from json import loads, dumps

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QSpinBox, QDateEdit, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox

PATH_TO_DATA_FILE = 'data.json'


class ViewCardWin(QMainWindow):
    def __init__(self, parent, card):
        super().__init__()
        uic.loadUi('ui/AddCardWin.ui', self)
        self.pushButton_2.hide()
        self.pushButton.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.save_data)
        self.par = parent
        self.lineEdit.setText(card['title']['serial'])
        self.lineEdit_2.setText(card['title']['number'])
        self.lineEdit_3.setText(card['title']['last_name'])
        self.lineEdit_4.setText(card['title']['first_name'])
        self.lineEdit_5.setText(card['title']['patronymic'])

        try:
            self.dateEdit.setDate(datetime.datetime.strptime(card['title']['birthday'], '%Y-%m-%d'))
        except Exception:
            pass

        try:
            self.dateEdit_2.setDate(datetime.datetime.strptime(card['title']['issue_date'], '%Y-%m-%d'))
        except Exception:
            pass

        self.lineEdit_6.setText(card['title']['profession'])
        self.lineEdit_7.setText(card['title']['education'])

        self.make_table(card)

        self.card_info = card
        self.pushButton_4.clicked.connect(self.add_row)
        self.tableWidget.verticalHeader().setVisible(False)
        self.widget.setVisible(False)

        self.pushButton_5.clicked.connect(self.dump_data)
        self.pushButton_6.clicked.connect(self.delete_work_book)

        self.tableWidget.setHorizontalHeaderLabels(['№ Записи', 'Дата', 'Сведенья', 'Документ', 'Удаление'])

        QTimer.singleShot(100, self.resize_table)

    def delete_work_book(self):
        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            data = loads(file.read())

        card_info = list(filter(lambda card: card['uuid'] == self.card_info['uuid'], data))[0]

        del data[data.index(card_info)]

        with open(PATH_TO_DATA_FILE, 'w', encoding='utf-8') as write_file:
            write_file.write(dumps(data))

        self.par.show()
        self.close()

    def dump_data(self):
        self.save_data()

        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Выберите путь сохранения", options=options)
        if directory:
            dump_data_json = self.card_info.copy()
            if 'uuid' in dump_data_json:
                del dump_data_json['uuid']
            file_name = os.path.join(directory,
                                     f'{dump_data_json["title"]["last_name"]}_{dump_data_json["title"]["first_name"]}.json')
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(dumps(dump_data_json))

            QMessageBox.information(self, 'Данные выгружены', 'Данные успешно выгружены в файл')

    def make_table(self, card):
        self.tableWidget.clear()

        self.tableWidget.setRowCount(len(card['job']))

        for row in range(len(card['job'])):
            number_spin_box = QSpinBox(self)
            number_spin_box.setMinimum(1)
            number_spin_box.setMaximum(100000)
            number_spin_box.setValue(card['job'][row]['number'])
            self.tableWidget.setCellWidget(row, 0, number_spin_box)
            date_edit = QDateEdit()
            date_edit.setDate(datetime.date.today())
            date_edit.setMaximumDate(datetime.date.today())
            date_edit.setCalendarPopup(True)

            try:
                date_edit.setDate(datetime.datetime.strptime(card['job'][row]['date'], '%Y-%m-%d'))
            except Exception:
                pass

            self.tableWidget.setCellWidget(row, 1, date_edit)
            self.tableWidget.setItem(row, 2, QTableWidgetItem(card['job'][row]['job_info']))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(card['job'][row]['basis']))

            delete_button = QPushButton()
            delete_button.setText('Удалить')
            delete_button.row = row
            delete_button.clicked.connect(self.delete_row)
            self.tableWidget.setCellWidget(row, 4, delete_button)

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
        with open(PATH_TO_DATA_FILE, 'r', encoding='utf-8') as file:
            data = loads(file.read())

        card_info = list(filter(lambda card: card['uuid'] == self.card_info['uuid'], data))[0]

        data[data.index(card_info)] = {
            "uuid": self.card_info['uuid'],
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

        self.card_info = {
            "uuid": self.card_info['uuid'],
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

        with open(PATH_TO_DATA_FILE, 'w', encoding='utf-8') as write_file:
            write_file.write(dumps(data))

    def back(self):
        self.par.show()
        self.close()
