from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from .schedule_view import ScheduleView
from .content_window import ContentWindow
from .schedule_editor import ScheduleEditorView

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

        # Создаем окна заранее, но не показываем
        self.schedule_view = None
        self.schedule_editor = None  # Добавляем окно редактора расписания
        self.content_window = None

    def open_content(self, title, content):
        self.hide()
        if title == "Расписание":
            if self.schedule_view is None:
                self.schedule_view = ScheduleView(go_back_callback=self.show_main_window)
            self.schedule_view.showMaximized()

        elif title == "Изменить расписание":
            if self.schedule_editor is None:
                self.schedule_editor = ScheduleEditorView(go_back_callback=self.show_main_window)
            self.schedule_editor.showMaximized()

        else:
            self.content_window = ContentWindow(title, content, self.show_main_window)
            self.content_window.showMaximized()

    def show_main_window(self):
        if self.schedule_view:
            self.schedule_view.hide()
        if self.schedule_editor:
            self.schedule_editor.hide()
        if self.content_window:
            self.content_window.hide()
        self.show()
