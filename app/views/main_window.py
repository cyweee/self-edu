from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout, QStyle, QTabWidget, QDialog, QComboBox, QMessageBox
)
from app.views.schedule_view import ScheduleView
from app.views.content_window import ContentWindow
from app.views.schedule_editor import ScheduleEditorView
from app.views.todo_view import TodoView
from app.views.useful_links_view import UsefulLinksView
from app.views.useful_links_view import get_all_links
from app.logic.language import translations
import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = self.load_lang()
        self.setup_header()
        self.setWindowTitle(self.tr("Self-Edu"))
        self.resize(1920, 1080)

        print(f"Загруженный язык: {self.lang}")

        # Атрибуты интерфейса
        self.schedule_view = None
        self.schedule_editor = None
        self.content_window = None
        self.todo_view = None
        self.useful_links_view = None

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setStyleSheet("background-color: #2C2C2C;")

        self.main_layout = QVBoxLayout(self.central)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)

        self.main_layout.addWidget(self.setup_header())

        self.menu_container = QWidget()
        self.menu_layout = QHBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(100, 50, 100, 50)
        self.menu_layout.setSpacing(50)

        self.card_texts = [
            ("Расписание", "Здесь будет расписание"),
            ("Изменить расписание", "Настройка расписания"),
            ("To-Do", "Список задач"),
            ("Полезные ссылки", "Ресурсы для обучения")
        ]

        self.menu_buttons = []
        for title, content in self.card_texts:
            btn = QPushButton(self.tr(title))
            btn.setMinimumSize(300, 300)
            btn.setStyleSheet("""QPushButton {
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
            }""")
            btn.clicked.connect(lambda checked, t=title, c=content: self.open_content(t, c))
            self.menu_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        self.main_layout.addWidget(self.menu_container, 1)
        self.main_layout.addStretch()

    def tr(self, key):
        return translations.get(self.lang, {}).get(key, key)

    def setup_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)

        self.logo_label = QLabel()
        self.load_logo()
        layout.addWidget(self.logo_label)

        self.title_label = QLabel(self.tr("Self-Edu"))
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding-left: 10px;")
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.header = header
        self.setup_settings_button()

        return header

    def load_logo(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "self-edu-logo.png"))

            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"{self.tr('Файл не найден')}: {logo_path}")

            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                raise ValueError(self.tr("Pixmap пустой — возможно, повреждён файл"))

            pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        except Exception as e:
            print(f"{self.tr('Ошибка загрузки логотипа')}: {e}")
            fallback_icon = self.style().standardIcon(QStyle.SP_DesktopIcon)
            self.logo_label.setPixmap(fallback_icon.pixmap(64, 64))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()
            return
        super().keyPressEvent(event)

    def setup_settings_button(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "settings.png"))

            if not os.path.exists(icon_path):
                raise FileNotFoundError(f"{self.tr('Файл не найден')}: {icon_path}")

            icon = QIcon(icon_path)
            if icon.isNull():
                raise ValueError(self.tr("Иконка пустая — возможно, повреждён файл"))

            self.settings_btn = QPushButton()
            self.settings_btn.setIcon(icon)
            self.settings_btn.setFixedSize(64, 64)
            self.settings_btn.clicked.connect(self.show_settings)
            self.header.layout().addWidget(self.settings_btn)

        except Exception as e:
            print(f"{self.tr('Ошибка загрузки иконки настроек')}: {e}")
            fallback_icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
            self.settings_btn = QPushButton()
            self.settings_btn.setIcon(fallback_icon)
            self.settings_btn.setFixedSize(64, 64)
            self.settings_btn.clicked.connect(self.show_settings)
            self.header.layout().addWidget(self.settings_btn)

    def toggle_theme(self):
        print(self.tr("Смена темы пока не реализована."))

    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Настройки"))
        dialog.setFixedSize(400, 300)

        dialog.setStyleSheet("""QDialog { background-color: #2C2C2C; color: white; }
            QLabel { color: white; }
            QPushButton {
                background-color: #3F51B5; color: white; border: none;
                padding: 6px 12px; border-radius: 6px;
            }
            QPushButton:hover { background-color: #5C6BC0; }
            QPushButton:pressed { background-color: #7986CB; }
            QTabWidget::pane { border: 1px solid #555; }
            QTabBar::tab {
                background: #444; color: white; padding: 6px 12px;
                border-top-left-radius: 4px; border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { background: #666; }
        """)

        tabs = QTabWidget()

        hotkeys_tab = QWidget()
        hotkeys_layout = QVBoxLayout()
        hotkeys_layout.addWidget(QLabel(f"<b>{self.tr('Горячие клавиши')}:</b>"))
        hotkeys_layout.addSpacing(10)

        hotkeys = [
            ("Enter", self.tr("Сохранить/Добавить")),
            ("Shift + Enter", self.tr("Добавить задачу")),
            ("Esc", self.tr("Назад к главному окну"))
        ]
        for key, action in hotkeys:
            label = QLabel(f"<code>{key}</code> — {action}")
            label.setStyleSheet("font-size: 14px;")
            hotkeys_layout.addWidget(label)
        hotkeys_tab.setLayout(hotkeys_layout)
        tabs.addTab(hotkeys_tab, self.tr("Горячие клавиши"))

        theme_tab = QWidget()
        theme_layout = QVBoxLayout()
        self.theme_switch = QPushButton(self.tr("Светлая тема"))
        self.theme_switch.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_switch)
        theme_tab.setLayout(theme_layout)
        tabs.addTab(theme_tab, self.tr("Тема"))

        lang_tab = QWidget()
        lang_layout = QVBoxLayout()
        label = QLabel(self.tr("Выберите язык:"))
        label.setStyleSheet("font-size: 14px;")
        lang_layout.addWidget(label)

        lang_selector = QComboBox()
        lang_selector.addItems(["Русский", "English"])
        codes = ["ru", "en"]

        if hasattr(self, "lang") and self.lang in codes:
            lang_selector.setCurrentIndex(codes.index(self.lang))

        # Вложенная функция с передачей dialog по умолчанию
        def handle_language_change(index, dialog=dialog):
            new_lang = codes[index]
            self.lang = new_lang
            self.set_language(new_lang)
            self.retranslate_ui()

            confirm = QMessageBox.question(
                self,
                self.tr("Сохранить язык"),
                self.tr("Сделать выбранный язык языком по умолчанию?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                self.save_lang(new_lang)

            dialog.close()

        lang_selector.currentIndexChanged.connect(handle_language_change)
        lang_layout.addWidget(lang_selector)

        lang_tab.setLayout(lang_layout)
        tabs.addTab(lang_tab, self.tr("Язык"))

        main_layout = QVBoxLayout(dialog)
        main_layout.addWidget(tabs)
        dialog.setLayout(main_layout)
        dialog.exec_()

    def save_lang(self, lang_code):
        config_dir = os.path.normpath(os.path.join(os.path.expanduser("~"), ".config", "self-edu"))
        os.makedirs(config_dir, exist_ok=True)
        settings_path = os.path.normpath(os.path.join(config_dir, "settings.json"))

        with open(settings_path, "w") as f:
            json.dump({"lang": lang_code}, f)

    def load_lang(self):
        config_dir = os.path.normpath(os.path.join(os.path.expanduser("~"), ".config", "self-edu"))
        settings_path = os.path.normpath(os.path.join(config_dir, "settings.json"))

        try:
            with open(settings_path, "r") as f:
                return json.load(f).get("lang", "ru")
        except:
            return "ru"

    def retranslate_ui(self):
        # Обновляем заголовок окна
        self.setWindowTitle(self.tr("Self-Edu"))
        # Обновляем заголовок и текст в header
        self.title_label.setText(self.tr("Self-Edu"))
        # Обновляем текст кнопок меню
        for btn, (title, _) in zip(self.menu_buttons, self.card_texts):
            btn.setText(self.tr(title))
        # Обновляем текст кнопки темы в настройках, если она есть
        if hasattr(self, 'theme_switch'):
            self.theme_switch.setText(self.tr("Светлая тема"))

    def set_language(self, lang):
        self.lang = lang

        if self.schedule_view is not None:
            self.schedule_view.set_language(lang)
        if self.schedule_editor is not None:
            self.schedule_editor.set_language(lang)
        if self.todo_view is not None:
            self.todo_view.set_language(lang)
        if self.useful_links_view is not None:
            self.useful_links_view.set_language(lang)
        if self.content_window is not None:
            self.content_window.set_language(lang)

        self.retranslate_ui()

    def open_content(self, title, content):
        self.hide()
        if title == "Расписание":
            if self.schedule_view is None:
                self.schedule_view = ScheduleView(go_back_callback=self.show_main_window, lang=self.lang)
            self.schedule_view.showMaximized()
            self.schedule_view.refresh()

        elif title == "Изменить расписание":
            if self.schedule_editor is None:
                self.schedule_editor = ScheduleEditorView(
                    go_back_callback=self.show_main_window,
                    schedule_view_ref=self.schedule_view,
                    lang=self.lang
                )
            self.schedule_editor.showMaximized()

        elif title == "To-Do":
            if self.todo_view is None:
                self.todo_view = TodoView(go_back_callback=self.show_main_window, lang=self.lang)
            self.todo_view.showMaximized()
            self.todo_view.load_tasks()

        elif title == "Полезные ссылки":
            if self.useful_links_view is None:
                self.useful_links_view = UsefulLinksView(go_back_callback=self.show_main_window, lang=self.lang)
            self.useful_links_view.showMaximized()
            self.useful_links_view.load_links()

    def show_main_window(self):
        for view in [
            self.schedule_view,
            self.schedule_editor,
            self.content_window,
            self.todo_view,
            self.useful_links_view
        ]:
            if view:
                view.hide()
        self.show()