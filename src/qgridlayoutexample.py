from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GrindProject')
        self.setGeometry(100, 100, 600, 400)

        self.glayout = QGridLayout()

        for y in range(0, 10):
            for x in range(0, 10):
                if x == y:
                    label = QLabel(f'Test label: {x}, {y}', self)
                    self.glayout.addWidget(label, x, y)

        self.glayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        central_widget = QWidget()
        central_widget.setLayout(self.glayout)
        self.setCentralWidget(central_widget)

        self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
