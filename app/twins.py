from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
import sys

class DropLabel(QLabel):
    def __init__(self, texto_inicial):
        super().__init__(texto_inicial)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px dashed gray; padding: 20px;")
        self.arquivos = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.arquivos = [url.toLocalFile() for url in event.mimeData().urls()]
            self.setText("\n".join(self.arquivos))
        else:
            self.setText("drop inválido")
            self.arquivos = []

class TwinsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twins")
        self.setGeometry(100, 100, 600, 400)

        layout_geral = QVBoxLayout()
        layout_dropzones = QHBoxLayout()

        # Campos de drag and drop
        self.label_esquerdo = DropLabel("original")
        self.label_direito = DropLabel("cópia")

        layout_dropzones.addWidget(self.label_esquerdo)
        layout_dropzones.addWidget(self.label_direito)

        # Botão
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_adicionar.clicked.connect(self.adicionar_caminhos)

        # Campo de texto editável
        self.campo_texto = QTextEdit()
        self.campo_texto.setPlaceholderText("Relação entre original e cópia...")

        # Monta layout
        layout_geral.addLayout(layout_dropzones)
        layout_geral.addWidget(self.botao_adicionar)
        layout_geral.addWidget(self.campo_texto)

        self.setLayout(layout_geral)

    def adicionar_caminhos(self):
        originais = self.label_esquerdo.arquivos
        copias = self.label_direito.arquivos

        # Evita erros se algum estiver vazio
        quantidade = min(len(originais), len(copias))
        if quantidade == 0:
            return

        linhas = []
        for i in range(quantidade):
            linhas.append(f'"{originais[i]}": "{copias[i]}"')

        texto_existente = self.campo_texto.toPlainText()
        if texto_existente.strip():
            texto_novo = texto_existente + "\n" + "\n".join(linhas)
        else:
            texto_novo = "\n".join(linhas)

        self.campo_texto.setPlainText(texto_novo)

app = QApplication(sys.argv)
janela = TwinsWindow()
janela.show()
sys.exit(app.exec())
