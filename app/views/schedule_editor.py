from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QSizePolicy, QSpacerItem,
    QHeaderView, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class ScheduleEditorView(QWidget):
    lesson_description_requested = Signal(int, int)  # Сигнал для запроса описания пары (row, col)

    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setWindowTitle("Редактор расписания")
        self.resize(1200, 800)

        self.num_days = 6  # Понедельник-Суббота
        self.num_slots = 6  # Максимум 6 пар в день

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("Редактор расписания")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        layout.addWidget(title_label)

        # Таблица: дни + заголовок
        self.table = QTableWidget(self.num_days + 1, self.num_slots + 1)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
            QTableWidget QLineEdit {
                font-size: 15px;
                color: white;
                background-color: #2C2C2C;
            }
        """)

        # Настройка заголовков
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        # Левая верхняя ячейка пустая
        self.table.setItem(0, 0, QTableWidgetItem(""))

        # Дни недели (первый столбец)
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        for row in range(1, self.num_days + 1):
            item = QTableWidgetItem(days[row - 1])
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)

        # Временные слоты (верхняя строка)
        for col in range(1, self.num_slots + 1):
            item = QTableWidgetItem("{time_of_lesson}")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, col, item)

        # Пустые редактируемые ячейки
        for row in range(1, self.num_days + 1):
            for col in range(1, self.num_slots + 1):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

        # Настройка размеров
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Особый стиль для первого столбца (дни недели)
        self.table.setColumnWidth(0, 150)  # Фиксированная ширина для дней

        # Обработчики событий
        self.table.cellChanged.connect(self.handle_cell_changed)
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)

        layout.addWidget(self.table)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

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
        btn_save.clicked.connect(self.save_schedule)
        button_layout.addWidget(btn_save)

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
        button_layout.addWidget(btn_back)

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(button_layout)

        self.setStyleSheet("background-color: #2C2C2C;")

        # Хранилище для описаний пар
        self.lesson_descriptions = {}
        for row in range(1, self.num_days + 1):
            for col in range(1, self.num_slots + 1):
                self.lesson_descriptions[(row, col)] = ""

    def handle_cell_changed(self, row, col):
        """Обработчик изменения ячейки"""
        if row > 0 and col > 0:  # Только для ячеек с предметами
            item = self.table.item(row, col)
            if item:
                text = item.text()
                # Автоматически делаем первую букву заглавной
                if text and text[0].islower():
                    item.setText(text[0].upper() + text[1:])

    def handle_cell_double_click(self, row, col):
        """Обработчик двойного клика для редактирования описания"""
        if row > 0 and col > 0:  # Только для ячеек с предметами
            self.edit_lesson_description(row, col)

    def edit_lesson_description(self, row, col):
        """Редактирование описания пары"""
        current_description = self.lesson_descriptions.get((row, col), "")

        # Получаем название предмета
        subject_item = self.table.item(row, col)
        subject = subject_item.text() if subject_item else ""

        # Создаем диалоговое окно для редактирования
        dialog = QMessageBox(self)
        dialog.setWindowTitle(f"Описание пары: {subject}")
        dialog.setText("Введите описание пары:")
        dialog.setIcon(QMessageBox.Information)

        # Добавляем поле для ввода текста
        dialog.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Save)

        # Создаем текстовое поле
        text_edit = QTextEdit()
        text_edit.setPlainText(current_description)
        text_edit.setMinimumSize(400, 200)

        # Вставляем текстовое поле в диалог
        layout = dialog.layout()
        layout.addWidget(text_edit, 1, 1)

        # Показываем диалог
        result = dialog.exec()

        if result == QMessageBox.Save:
            new_description = text_edit.toPlainText()
            self.lesson_descriptions[(row, col)] = new_description
            # Можно добавить визуальный индикатор, что у пары есть описание
            if new_description:
                subject_item.setBackground(Qt.darkGreen)
            else:
                subject_item.setBackground(Qt.transparent)

    def save_schedule(self):
        """Сохранение расписания"""
        print("Сохраняем расписание...")
        schedule = {}
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        times = []

        # Собираем времена пар из первой строки
        for col in range(1, self.num_slots + 1):
            item = self.table.item(0, col)
            times.append(item.text() if item else "{time_of_lesson}")

        # Собираем расписание по дням
        for row in range(1, self.num_days + 1):
            day_schedule = []
            for col in range(1, self.num_slots + 1):
                item = self.table.item(row, col)
                lesson = {
                    "subject": item.text() if item else "",
                    "time": times[col - 1],
                    "description": self.lesson_descriptions.get((row, col), "")
                }
                day_schedule.append(lesson)
            schedule[days[row - 1]] = day_schedule

        print("Текущее расписание:", schedule)
        QMessageBox.information(self, "Сохранено", "Расписание успешно сохранено!")