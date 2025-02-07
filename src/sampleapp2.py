from PySide6.QtGui import QAction, QFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy,
    QFileDialog,
    QTextEdit,
    QMenuBar,
    QWidget,
    QLabel,
    QFrame
)
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SampleApp2')
        self.setGeometry(100, 100, 600, 400)

        # self.setStyleSheet('border: 2px solid red')

        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu('File')

        new_action = QAction('new', self)
        open_action = QAction('open', self)
        close_action = QAction('close', self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)

        new_action.triggered.connect(self.new_action_handler)
        open_action.triggered.connect(self.open_action_handler)
        close_action.triggered.connect(self.close_action_handler)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        main_layout.addWidget(menu_bar)

        container_layout = QGridLayout()
        container_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        hline_1 = QFrame(self)
        hline_1.setFrameShape(QFrame.HLine)

        hline_1.setLineWidth(4)
        main_layout.addWidget(hline_1)

        fs_layout = QGridLayout()
        fs_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        note_layout = QVBoxLayout()
        note_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        vline = QFrame(self)
        vline.setFrameShape(QFrame.VLine)

        vline.setLineWidth(4)
        container_layout.addLayout(fs_layout, 0, 0)

        container_layout.addWidget(vline, 0, 1)
        container_layout.addLayout(note_layout, 0, 2)

        main_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.addLayout(container_layout)

        hline_2 = QFrame(self)
        hline_2.setFrameShape(QFrame.HLine)

        hline_2.setLineWidth(4)
        hline_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.char_count_label = QLabel('Char count: 0')
        self.char_count_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        main_layout.addWidget(hline_2)
        main_layout.addWidget(self.char_count_label)

        for n in range(20):
            new_label = QLabel(f'A text {n}')
            new_label.setStyleSheet('color: red; font-size: 12px')

            # ...
            fs_layout.addWidget(new_label, n, 0)

        self.text_pane = QTextEdit()
        self.text_pane.textChanged.connect(
            self.update_char_count
        )
        self.text_pane.setFont(QFont('Arial', 12))

        note_layout.addWidget(self.text_pane)

    def update_char_count(self):
        n = len(self.text_pane.toPlainText())
        self.char_count_label.setText(f'Char count: {n}')

    def new_action_handler(self):
        pass

    def open_action_handler(self):
        options = QFileDialog.Options()
        fpath_s, _ = QFileDialog.getOpenFileName(
            self,
            'Open file',
            '/home',
            'All files (*);;Text Files (*.txt)',
            options=options
        )

    def close_action_handler(self):
        pass

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())