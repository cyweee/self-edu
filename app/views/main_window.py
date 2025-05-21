from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout, QApplication
)
from PySide6.QtCore import Qt
import sys


class ContentWindow(QMainWindow):
    def __init__(self, title: str, content: str, go_back_callback):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(0, 0, 1920, 1080)

        self.go_back_callback = go_back_callback

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #2C2C2C;")

        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        btn_back = QPushButton("← Назад")
        btn_back.setFixedSize(140, 40)
        btn_back.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
        """)
        btn_back.clicked.connect(self.back)

        label = QLabel(content, alignment=Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 32px; color: white;")

        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

    def back(self):
        self.go_back_callback()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Self-Edu")
        self.resize(1920, 1080)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setStyleSheet("background-color: #2C2C2C;")

        layout = QHBoxLayout(self.central)
        layout.setContentsMargins(100, 200, 100, 200)
        layout.setSpacing(50)

        card_texts = [
            ("Расписание", "Здесь будет расписание"),
            ("Изменить расписание", "Настройка расписания"),
            ("To-Do", "Список задач"),
            ("Полезные ссылки", "Ресурсы для обучения")
        ]

        for title, content in card_texts:
            btn = QPushButton(title)
            btn.setMinimumSize(300, 300)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    color: #FFFFFF;
                    border: 2px solid #3F51B5;
                    border-radius: 15px;
                    background-color: #3F51B5;
                }
                QPushButton:hover {
                    background-color: #5C6BC0;
                    border: 2px solid #5C6BC0;
                }
                QPushButton:pressed {
                    background-color: #7986CB;
                    border: 2px solid #7986CB;
                }
            """)
            btn.clicked.connect(lambda checked, t=title, c=content: self.open_content(t, c))
            layout.addWidget(btn)

    def open_content(self, title, content):
        self.hide()
        self.content_window = ContentWindow(title, content, self.show)
        self.content_window.showMaximized()