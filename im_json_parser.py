import sys, json
import pandas as pd
import time
from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit, QPushButton, QTableWidget, QVBoxLayout, QHeaderView, \
    QApplication, QTableWidgetItem, QWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.df = None

        self.setWindowTitle('IM_JSON2csv')
        self.setGeometry(1000, 50, 800, 800)

        self.key_list = QLineEdit(self)
        self.key_list.setText('output_object result')
        self.json_content = QPlainTextEdit(self)

        self.btn1 = QPushButton('step1. json 변환', self)
        self.btn1.clicked.connect(self.button_event)

        self.btn2 = QPushButton('step2. tsv로 저장', self)
        self.btn2.clicked.connect(self.save_into_tsv)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(300, 300)
        # self.tableWidget.setSortingEnabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.key_list)
        layout.addWidget(self.json_content)
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

            df = pd.DataFrame(json_content)

            self.tableWidget.setRowCount(len(json_content))
            self.tableWidget.setColumnCount(len(df.columns))
            self.tableWidget.setHorizontalHeaderLabels(df.columns)
            header = self.tableWidget.horizontalHeader()

            for i in range(0, len(json_content)):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                for j in range(0, len(df.columns)):
                    temp = str(df.iloc[i, j])
                    self.tableWidget.setItem(i, j, QTableWidgetItem(temp))
                    # self.tableWidget.item(i, j).setTextAlignment()

            self.df = df
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
