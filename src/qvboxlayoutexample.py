import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GrindProject')
        self.setGeometry(100, 100, 600, 400)

        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.button_clicked)

        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.button)

        self.vlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        central_widget = QWidget()
        central_widget.setStyleSheet('border: 2px solid pink;')
        central_widget.setLayout(self.vlayout)
        self.setCentralWidget(central_widget)

    def button_clicked(self):
        new_label = QLabel('Button test', self)
        new_label.setStyleSheet('font-size: 24px; color: lime;')
        new_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.vlayout.insertWidget(1, new_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
