from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QSizePolicy, QSpacerItem,
    QHeaderView, QMessageBox, QTextEdit, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class ScheduleEditorView(QWidget):
    lesson_description_requested = Signal(int, int)

    def __init__(self, go_back_callback, schedule_view_ref):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setWindowTitle("Редактор расписания")
        self.resize(1200, 800)

        self.num_days = 6  # Понедельник-Суббота
        self.num_slots = 5  # 5 пар в день
        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

        self.init_ui()
        self.lesson_descriptions = {}

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Заголовок
        title_label = QLabel("Редактор расписания")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        layout.addWidget(title_label)

        # Таблица
        self.init_table()
        layout.addWidget(self.table)

        # Кнопки
        self.init_buttons(layout)

        self.setStyleSheet("background-color: #2C2C2C;")

    def keyPressEvent(self, event):
        # Только Esc - назад
        if event.key() == Qt.Key_Escape and self.go_back_callback:
            self.go_back_callback()
            return

        super().keyPressEvent(event)

    def init_table(self):
        self.table = QTableWidget(self.num_days + 1, self.num_slots + 1)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Стилизация таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1E1E1E;
                color: white;
                font-size: 15px;
                gridline-color: #3F51B5;
                border: 2px solid #3F51B5;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        # Заполняем таблицу
        self.fill_table()

        # Подключаем обработчики событий
        self.table.cellDoubleClicked.connect(self.handle_double_click)

    def fill_table(self):
        from app.logic.schedule import get_full_schedule  # Импорт функции получения данных

        # Загружаем сохраненное расписание из БД
        schedule_data = get_full_schedule()

        # Заполняем шапку с номерами пар (первая строка)
        for col in range(1, self.num_slots + 1):
            item = QTableWidgetItem(f"Пара {col}")
            item.setFlags(Qt.ItemIsEnabled)  # Запрещаем редактирование
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, col, item)

        # Заполняем первый столбец с днями недели
        for row in range(1, self.num_days + 1):
            item = QTableWidgetItem(self.days[row - 1])
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)

        # Заполняем ячейки с предметами
        for row in range(1, self.num_days + 1):
            for col in range(1, self.num_slots + 1):
                # Ищем предмет для текущей ячейки
                subject = next((item["subject"] for item in schedule_data
                                if item["day"] == self.days[row - 1] and item["time_slot"] == col), "")
                item = QTableWidgetItem(subject)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

        # Настройка размеров
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 150)

    def init_buttons(self, layout):
        # Создаем контейнер для кнопок
        buttons_container = QWidget()
        buttons_container.setStyleSheet("background: transparent;")
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(30)

        # Добавляем растягивающийся элемент слева
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Кнопка Сохранить
        btn_save = QPushButton("Сохранить")
        btn_save.setFixedSize(160, 50)
        btn_save.setStyleSheet("""
            QPushButton {
                font-size: 18px; 
                color: white; 
                background-color: #3F51B5; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
        """)
        btn_save.clicked.connect(self.on_save_clicked)
        buttons_layout.addWidget(btn_save)

        # Кнопка Назад
        btn_back = QPushButton("Назад")
        btn_back.setFixedSize(160, 50)
        btn_back.setStyleSheet("""
            QPushButton {
                font-size: 18px; 
                color: white; 
                background-color: #3F51B5; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
        """)
        btn_back.clicked.connect(self.go_back_callback)
        buttons_layout.addWidget(btn_back)

        # Кнопка Очистить
        btn_clear = QPushButton("Очистить")
        btn_clear.setFixedSize(160, 50)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border-radius: 10px;
            }
        """)
        btn_clear.clicked.connect(self.clear_schedule)
        buttons_layout.addWidget(btn_clear)

        # Добавляем растягивающийся элемент справа
        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Добавляем контейнер с кнопками в основной layout
        layout.addWidget(buttons_container)

    def clear_schedule(self):
        """Полностью очищает расписание (БД + интерфейс)"""
        try:
            from app.logic.schedule import clear_schedule

            # 1. Очищаем базу данных
            clear_schedule()

            # 2. Очищаем таблицу в интерфейсе
            for row in range(1, self.num_days + 1):
                for col in range(1, self.num_slots + 1):
                    if item := self.table.item(row, col):
                        item.setText("")

            # 3. Очищаем описания уроков
            self.lesson_descriptions.clear()

            # 4. Обновляем отображение
            self.table.viewport().update()

            # 5. Обновляем schedule_view (если он открыт)
            if hasattr(self, 'schedule_view_ref') and self.schedule_view_ref:
                self.schedule_view_ref.refresh()

            QMessageBox.information(self, "Успех", "Расписание полностью очищено!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка очистки: {str(e)}")
    def handle_double_click(self, row, col):
        """Обработчик двойного клика"""
        if row > 0 and col > 0:  # Только для ячеек с предметами
            self.edit_lesson_description(row, col)

    def edit_lesson_description(self, row, col):
        """Редактирование описания пары"""
        current_description = self.lesson_descriptions.get((row, col), "")
        subject_item = self.table.item(row, col)
        subject = subject_item.text() if subject_item else ""

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Описание пары: {subject}")
        dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setPlainText(current_description)
        text_edit.setFocus()  # Установить фокус сразу

        # Переопределение нажатия клавиш
        def handle_key(event):
            if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not (event.modifiers() & Qt.ShiftModifier):
                dialog.accept()
            else:
                QTextEdit.keyPressEvent(text_edit, event)

        text_edit.keyPressEvent = handle_key

        layout.addWidget(text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.Accepted:
            new_description = text_edit.toPlainText()
            self.lesson_descriptions[(row, col)] = new_description
            if new_description:
                subject_item.setBackground(QColor("#2E7D32"))  # Зеленый фон
            else:
                subject_item.setBackground(QColor("#1E1E1E"))  # Стандартный фон

    def on_save_clicked(self):
        try:
            from app.logic.schedule import save_schedule_item

            # Сохраняем данные для каждого дня и слота (без времени)
            for row in range(1, self.num_days + 1):
                day = self.days[row - 1]
                for col in range(1, self.num_slots + 1):
                    subject_item = self.table.item(row, col)
                    if subject_item and subject_item.text().strip():
                        save_schedule_item(
                            day=day,
                            time_slot=col,
                            subject=subject_item.text(),
                            topic=self.lesson_descriptions.get((row, col), "")
                        )

            QMessageBox.information(self, "Успех", "Расписание сохранено!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")