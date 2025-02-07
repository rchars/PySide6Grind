from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QWidget,
    QLabel,
    QFrame
)
import requests
import random
import time
import sys

class MainWindow(QWidget):
    MAX_SAMPLE_LEN = 64
    REFRESH_INTERVAL = 15000

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.labels = []
        for _ in range(25):
            new_label_1 = QLabel()
            new_label_2 = QLabel()

            new_label_1.setFixedWidth(128)
            new_label_2.setFixedWidth(128)

            new_layout = QHBoxLayout()
            new_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            main_layout.addLayout(new_layout)

            vline = QFrame()
            vline.setFrameShape(QFrame.VLine)
            vline.setLineWidth(2)

            new_layout.addWidget(new_label_1)
            new_layout.addWidget(new_label_2)
            new_layout.insertWidget(1, vline)

            self.labels.append([new_label_1, new_label_2])

        timer = QTimer(self)
        timer.timeout.connect(self.refresh_labels)
        timer.start(self.REFRESH_INTERVAL)

    def refresh_labels(self):
        res = requests.get('https://api.coinlore.net/api/tickers/', data={'start': 0, 'limit': 25})
        res_json = res.json()

        for i, label_pack in enumerate(self.labels):
            name = res_json['data'][i]['name']
            price_usd = res_json['data'][i]['price_usd']
            label_pack[0].setText(name)
            label_pack[1].setText(price_usd)

    # def keyPressEvent(self, event):
    #     self.refresh_labels()

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())