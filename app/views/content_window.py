from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.logic.language import translations

class ContentWindow(QMainWindow):
    def __init__(self, title: str, content: str, go_back_callback, lang="ru"):
        super().__init__()
        self.lang = lang
        self.setWindowTitle(self.tr(title))
        self.go_back_callback = go_back_callback

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)

        self.btn_back = QPushButton(f"← {self.tr('Назад')}")
        self.btn_back.clicked.connect(self.back)
        self.layout.addWidget(self.btn_back, alignment=Qt.AlignLeft)

        self.label = QLabel(self.tr(content), alignment=Qt.AlignCenter)
        self.layout.addWidget(self.label)

    def tr(self, key):
        return translations.get(self.lang, {}).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr(self.windowTitle()))
        self.btn_back.setText(f"← {self.tr('Назад')}")
        self.label.setText(self.tr(self.label.text()))

    def back(self):
        self.go_back_callback()
        self.close()
