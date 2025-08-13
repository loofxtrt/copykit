from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
import sys

class AppMain(QMainWindow):
    def __init__(self):
        # inicializar a classe pai
        super(AppMain, self).__init__()

        loadUi("app/ui/main.ui", self)
        self.find_widgets()
        self.configure_widgets()
        #self.create_match_row()

        

    def find_widgets(self):
        self.match_bar = self.findChild(QVBoxLayout, "matchBar")

    def configure_widgets(self):
        # fazer os itens da match bar serem listados de cima pra baixo
        self.match_bar.setAlignment(Qt.AlignmentFlag.AlignTop)

    def create_match_row(self, first_image_path: str = "app/icons/example-1.svg", second_image_path: str = "app/icons/example-2.svg"):
        # criar o container base pro row, que vai definir a altura fixa
        # isso é feito porque um hbox por si só nao tem essa propriedade
        row_container = QWidget()
        row_container.setFixedHeight(100)
        row_container.setMaximumWidth(700)
        row_container.setStyleSheet("background-color: rgba(255, 255, 255, 15);")

        # criar agora o row de verdade, que vai ser filho do row_container
        row = QHBoxLayout(row_container)
        
        def create_item(icon_path):
            # criar o label e o pixmap
            pixmap = QPixmap(icon_path)

            image = QLabel()
            image.setPixmap(pixmap)

            # criar o label que exibe o path em forma de texto
            # o if aqui é só pra tratar o caso especial de exemplo
            if icon_path.startswith("app/icons/"):
                file_name = icon_path.split("/")[2]
                icon_path = f"scalable/apps/{file_name}"

            path_text = QLabel(f"ICON_PACK/{icon_path}")

            # criar o layout do item que vai conter esses labels
            item = QVBoxLayout()
            item.addWidget(image)
            item.addWidget(path_text)

            # depois, criar o container do item, e setar que o layout dele vai ser o criado anteriormente
            item_container = QWidget()
            item_container.setLayout(item)

            return item_container

        # criar os itens
        label_1 = create_item(first_image_path)
        label_2 = create_item(second_image_path)

        # criar a seta entre os dois itens
        arrow_pixmap = QPixmap("app/icons/google/arrow_right_alt_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg")
        middle_arrow = QLabel()
        middle_arrow.setPixmap(arrow_pixmap)

        row.addWidget(label_1)
        row.addWidget(middle_arrow)
        row.addWidget(label_2)

        self.match_bar.addWidget(row_container)

app = QApplication(sys.argv)
window = AppMain()
window.show()
app.exec()
