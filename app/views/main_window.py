from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from app.views.schedule_view import ScheduleView
from app.views.content_window import ContentWindow
from app.views.schedule_editor import ScheduleEditorView
from app.views.todo_view import TodoView
from app.views.useful_links_view import UsefulLinksView
from app.views.useful_links_view import get_all_links

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Self-Edu")
        self.resize(1920, 1080)

        # Инициализируем все атрибуты
        self.schedule_view = None
        self.schedule_editor = None
        self.content_window = None
        self.todo_view = None
        self.useful_links_view = None

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
        if title == "Расписание":
            if self.schedule_view is None:
                self.schedule_view = ScheduleView(go_back_callback=self.show_main_window)
            self.schedule_view.showMaximized()
            self.schedule_view.refresh()
        elif title == "Изменить расписание":
            if self.schedule_editor is None:
                self.schedule_editor = ScheduleEditorView(
                    go_back_callback=self.show_main_window,
                    schedule_view_ref=self.schedule_view
                )
            self.schedule_editor.showMaximized()
        elif title == "To-Do":
            if self.todo_view is None:
                self.todo_view = TodoView(  # Без передачи ссылки
                    go_back_callback=self.show_main_window
                )
            self.todo_view.showMaximized()
            self.todo_view.load_tasks()  # Обновляем данные при открытии
        elif title == "Полезные ссылки":
            if self.useful_links_view is None:
                self.useful_links_view = UsefulLinksView(go_back_callback=self.show_main_window)
            self.useful_links_view.showMaximized()
            self.useful_links_view.load_links()

    def show_main_window(self):
        if self.schedule_view:
            self.schedule_view.hide()
        if self.schedule_editor:
            self.schedule_editor.hide()
        if self.content_window:
            self.content_window.hide()
        if self.todo_view:
            self.todo_view.hide()
        if self.useful_links_view:
            self.useful_links_view.hide()
        self.show()