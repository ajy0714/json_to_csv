import json
import sys
import time
import pandas as pd
from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit, QPushButton, QTableWidget, QVBoxLayout, QApplication, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.df = None

        self.setWindowTitle('IM_JSON2csv')
        self.setGeometry(1000, 50, 800, 800)

        self.key_list = QLineEdit(self)
        self.key_list.setPlaceholderText('추출하고자 값의 키를 공백으로 구분하여 입력하세요(ex. output_object result IM)')
        self.json_content = QPlainTextEdit(self)
        self.json_content.setPlaceholderText('JSON의 내용을 입력하세요')

        self.btn1 = QPushButton('step1. Convert into JSON', self)
        self.btn1.clicked.connect(self.button_event)

        self.btn2 = QPushButton('step2. Save as TSV file', self)
        self.btn2.clicked.connect(self.save_into_tsv)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(300, 300)

        layout = QVBoxLayout()
        layout.addWidget(self.json_content)
        layout.addWidget(self.key_list)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        self.setLayout(layout)
        self.show()

    def button_event(self):
        try:
            key_list = self.key_list.text().split(' ')
            json_content = json.loads(self.json_content.toPlainText())

            for i in key_list:
                json_content = json_content.get(i)

            self.df = pd.DataFrame(json_content)
            print(self.df)

            self.tableWidget.setRowCount(len(json_content))
            self.tableWidget.setColumnCount(len(self.df.columns))
            self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

            for i in range(0, len(json_content)):
                for j in range(0, len(self.df.columns)):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))
                    self.tableWidget.item(i, j).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            for i in range(0, len(self.df.columns)):
                self.tableWidget.resizeColumnToContents(i)

        except Exception as e:
            print('error occurred: ', e)

    def save_into_tsv(self):
        tm = time.localtime(time.time())
        file_name = "imCalcResult_" + str(tm.tm_year) + str(tm.tm_mon) + str(tm.tm_mday) + str(tm.tm_hour) + str(
            tm.tm_min) + str(tm.tm_sec) + '.tsv'
        self.df.to_csv(file_name, sep='\t')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())