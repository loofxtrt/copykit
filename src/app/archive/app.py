from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sys

class AppMain(QWidget):
    def __init__(self):
        # inicializar a classe pai
        super().__init__()

        self.setWindowTitle("Copykit")
        self.resize(1600, 900)

        side_vbox = QVBoxLayout()
        row_hbox = QHBoxLayout()

        label_1 = QLabel()
        example_1 = QPixmap("app/icons/example-1.svg")
        label_1.setPixmap(example_1)

        label_2 = QLabel()
        example_2 = QPixmap("app/icons/example-2.svg")
        label_2.setPixmap(example_2)

        row_hbox.addWidget(label_1)
        row_hbox.addWidget(label_2)

        side_vbox.addLayout(row_hbox)
        self.setLayout(side_vbox)

app = QApplication([])

window = AppMain()
window.show()

app.exec()
