from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout, QStyle
)
from app.views.schedule_view import ScheduleView
from app.views.content_window import ContentWindow
from app.views.schedule_editor import ScheduleEditorView
from app.views.todo_view import TodoView
from app.views.useful_links_view import UsefulLinksView
from app.views.useful_links_view import get_all_links
import os

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

        # Создаем центральный виджет и основной layout
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setStyleSheet("background-color: #2C2C2C;")

        # Основной вертикальный layout (вместо старого QHBoxLayout)
        self.main_layout = QVBoxLayout(self.central)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)  # Отступ между элементами

        # Добавляем хедер с логотипом
        self.main_layout.addWidget(self.setup_header())

        # Создаем контейнер для кнопок меню (старый HBoxLayout)
        self.menu_container = QWidget()
        self.menu_layout = QHBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(100, 50, 100, 50)  # Уменьшил отступы
        self.menu_layout.setSpacing(50)

        # Добавляем кнопки меню (ваш существующий код)
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
            self.menu_layout.addWidget(btn)

        # Добавляем контейнер с кнопками в основной layout
        self.main_layout.addWidget(self.menu_container, 1)  # Аргумент 1 - растягиваем по вертикали
        self.main_layout.addStretch()  # Добавляем растяжимое пространство снизу

    def setup_header(self):
        """Создает верхнюю панель с логотипом и названием"""
        header = QWidget()
        layout = QHBoxLayout(header)

        # Логотип
        self.logo_label = QLabel()
        self.load_logo()  # Загружаем изображение
        layout.addWidget(self.logo_label)

        # Название приложения
        self.title_label = QLabel("Self-Edu")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding-left: 10px;
        """)
        layout.addWidget(self.title_label)
        layout.addStretch()  # Выравниваем элементы влево

        return header

    def load_logo(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Папка, где main_window.py
            logo_path = os.path.join(base_dir, "..", "..", "assets", "self-edu-logo.png")
            logo_path = os.path.normpath(logo_path)

            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Файл не найден: {logo_path}")

            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                raise ValueError("Pixmap пустой — возможно, повреждён файл")

            pixmap = pixmap.scaled(64, 64,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            icon = self.style().standardIcon(QStyle.SP_DesktopIcon)
            self.logo_label.setPixmap(icon.pixmap(64, 64))

    def keyPressEvent(self, event):
        # Esc - ничего не делаем, чтобы не конфликтовало
        if event.key() == Qt.Key_Escape:
            event.ignore()
            return

        super().keyPressEvent(event)

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