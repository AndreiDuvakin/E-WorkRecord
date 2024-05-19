import datetime
import os
import uuid
from json import loads, dumps

import requests
from PyQt5 import uic
from PyQt5.QtCore import QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QSpinBox, QDateEdit, QPushButton, QTableWidgetItem, QFileDialog, QMessageBox, \
    QListWidgetItem, QRadioButton

from src.parse_text import parser_text
from view_card_window import ViewCardWin

PATH_TO_DATA_FILE = 'data.json'


class AddCardWin(QMainWindow):
    response_received = pyqtSignal(name='response_received')

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
        self.pushButton_6.setVisible(False)
        self.widget.setVisible(False)
        self.widget_2.setVisible(False)
        self.widget_3.setVisible(False)

        self.parsed_texts = []
        self.all_words = []

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

    def dump_data(self):
        card_info = {
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

        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Выберите путь сохранения", options=options)
        if directory:
            file_name = os.path.join(directory,
                                     f'{card_info["title"]["last_name"]}_{card_info["title"]["first_name"]}.json')
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(dumps(card_info))

            QMessageBox.information(self, 'Данные выгружены', 'Данные успешно выгружены в файл')

    def lets_scan(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)",
                                                   options=options)
        if file_name:
            self.all_words = []
            self.parsed_texts = []

            layout = self.widget_3.children()[0]
            count = layout.count()

            for i in range(count):
                item = layout.itemAt(i)
                if item.widget():
                    item.widget().close()

            self.image_path = file_name
            self.start_ocr_thread()
            pixmap = QPixmap(self.image_path)
            self.widget.setVisible(True)
            self.label_11.setPixmap(pixmap)

    def start_ocr_thread(self):
        self.ocr_thread = OCRThread(self.image_path)
        self.ocr_thread.ocr_completed.connect(self.on_ocr_completed)
        self.ocr_thread.start()

    def on_ocr_completed(self, result):
        if 'Error: ' in result[0]:
            QMessageBox.warning(self, 'Ошибка оцифровки', result[0])
            return

        self.widget_2.setVisible(True)
        self.widget_3.setVisible(True)

        layout = self.widget_3.children()[0]
        count = layout.count()

        for i in range(count):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().close()

        for variant_index in range(len(result)):
            parsed_text, all_word = parser_text(result[variant_index])
            self.parsed_texts.append(parsed_text)
            self.all_words.append(all_word)
            radio_button = QRadioButton()
            radio_button.setText(f'Вариант {str(variant_index + 1)}')
            radio_button.toggled.connect(self.render_result)
            radio_button.index = variant_index
            self.widget_3.children()[0].addWidget(radio_button)
            if variant_index == 0:
                radio_button.setChecked(True)

    def render_result(self):
        self.listWidget.clear()
        sender = self.sender()

        parsed_text = self.parsed_texts[sender.index]
        all_word = self.all_words[sender.index]

        self.lineEdit.setText(parsed_text['title']['serial'])
        self.lineEdit_2.setText(parsed_text['title']['number'])
        self.lineEdit_3.setText(parsed_text['title']['last_name'])
        self.lineEdit_4.setText(parsed_text['title']['first_name'])
        self.lineEdit_5.setText(parsed_text['title']['patronymic'])
        self.lineEdit_6.setText(parsed_text['title']['profession'])
        self.lineEdit_7.setText(parsed_text['title']['education'])

        for word in all_word:
            list_item = QListWidgetItem()
            list_item.setText(word)
            self.listWidget.addItem(list_item)

        self.resize_table()

    def back(self):
        self.par.show()
        self.close()


class OCRThread(QThread):
    ocr_completed = pyqtSignal(list, name='ocr_completed')

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        url = 'http://localhost:6543/recognition'
        files = {'image': open(self.image_path, 'rb')}

        try:
            response = requests.post(url, files=files)
        except Exception:
            text = [f"Error: Ошибка подключения к серверу"]
            self.ocr_completed.emit(text)
            return

        if response.status_code == 200:
            text = response.json()
        else:
            text = [f"Error: {response.status_code}"]
        self.ocr_completed.emit(text)
