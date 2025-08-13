import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap

from maps.replace import software
from src.utils.paths import COPYCAT_REPO_MAIN, SUBSTITUTES_APPS

APP_ROOT = "src/app"

class AppMain(QMainWindow):
    def __init__(self):
        # inicializar a classe pai
        super(AppMain, self).__init__()

        loadUi(f"{APP_ROOT}/ui/main.ui", self)
        self.find_widgets()
        self.configure_widgets()
        #self.create_match_row()

        for key, value in software.items():
            aliases = []
            
            # adicionar os outros aliases ao array de aliases caso o ignore key nao seja true
            if not value.get("ignore_key", False):
                aliases = [key]
                aliases.extend(value.get("aliases", []))
            else:
                aliases = value.get("aliases", [])

            for alias in aliases:
                # só criar rows pros ícones que existem
                source_path = COPYCAT_REPO_MAIN / f"apps/scalable{alias}"
                if source_path.is_file():
                    continue

                self.create_match_row(
                    str(COPYCAT_REPO_MAIN / "apps/scalable" / alias),
                    str(value["substitute"])
                )

    def find_widgets(self):
        # pegar a scrollArea e criar matchBar dentro do widget de conteúdo
        self.scroll_area = self.findChild(QScrollArea, "scrollArea")
        
        # criar o widget que vai ser conteúdo rolável
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        # criar o layout vertical dentro do conteúdo
        self.match_bar = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.match_bar)

    def configure_widgets(self):
        # fazer os itens da match bar serem listados de cima pra baixo
        self.match_bar.setAlignment(Qt.AlignmentFlag.AlignTop)

    def create_match_row(self, first_image_path: str = f"{APP_ROOT}/example-1.svg", second_image_path: str = f"{APP_ROOT}/example-2.svg"):
        # criar o container base pro row, que vai definir a altura fixa
        # isso é feito porque um hbox por si só nao tem essa propriedade
        row_container = QWidget()
        row_container.setFixedHeight(130)
        row_container.setMaximumWidth(1000)
        row_container.setStyleSheet("background-color: rgba(255, 255, 255, 15);")

        # criar agora o row de verdade, que vai ser filho do row_container
        row = QHBoxLayout(row_container)
        
        def create_item(icon_path):
            # criar o label e o pixmap
            pixmap = QPixmap(icon_path)

            # definir tamanho fixo igual pra todos os ícones
            icon_size = 32
            pixmap = pixmap.scaled(icon_size, icon_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            image = QLabel()
            image.setPixmap(pixmap)

            # criar o label que exibe o path em forma de texto
            path_text = QLabel(icon_path)
            path_text.setWordWrap(True)

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
        arrow_pixmap = QPixmap(f"{APP_ROOT}/icons/google/arrow_right_alt_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.svg")
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
