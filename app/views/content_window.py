from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class ContentWindow(QMainWindow):
    def __init__(self, title: str, content: str, go_back_callback):
        super().__init__()
        self.setWindowTitle(title)
        self.go_back_callback = go_back_callback

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(self.back)
        layout.addWidget(btn_back, alignment=Qt.AlignLeft)

        label = QLabel(content, alignment=Qt.AlignCenter)
        layout.addWidget(label)

    def back(self):
        self.go_back_callback()
        self.close()
