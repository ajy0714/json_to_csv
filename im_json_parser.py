import sys, json
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('IM_JSON2csv')
        self.setGeometry(1000,50,800,800)

        self.key_list = QLineEdit(self)
        self.json_content = QPlainTextEdit(self)

        self.btn1= QPushButton('제출',self)
        self.btn1.clicked.connect(self.button_event)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(300,300)
        self.tableWidget.setSortingEnabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.key_list)
        layout.addWidget(self.json_content)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.btn1)

        self.setLayout(layout)
        self.show()

    def button_event(self):
        key_list = self.key_list.text().split(' ')
        json_content = json.loads(self.json_content.toPlainText())

        for i in key_list:
            json_content=json_content.get(i)

        df=pd.DataFrame(json_content)
        df.to_csv('sample.tsv', sep='\t')

        self.tableWidget.setRowCount(len(json_content))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        header=self.tableWidget.horizontalHeader()

        for i in range(0, len(df.columns)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            for j in range(0,len(json_content)):
                self.tableWidget.setItem(i,j,QTableWidgetItem(df.iloc[i,j]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())