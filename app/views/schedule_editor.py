from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QSizePolicy, QSpacerItem,
    QHeaderView, QMessageBox, QTextEdit, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from app.logic.language import translations


class ScheduleEditorView(QWidget):
    lesson_description_requested = Signal(int, int)

    def __init__(self, go_back_callback, schedule_view_ref, lang = "ru"):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.schedule_view_ref = schedule_view_ref
        self.lang = lang
        self.setWindowTitle(self.tr("Редактор расписания"))
        self.resize(1200, 800)

        self.num_days = 6
        self.num_slots = 5
        self.days = [
            self.tr("Понедельник"), self.tr("Вторник"), self.tr("Среда"),
            self.tr("Четверг"), self.tr("Пятница"), self.tr("Суббота")
        ]

        self.lesson_descriptions = {}

        self.init_ui()

    def tr(self, key):
        return translations.get(self.lang, {}).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.retranslate_ui()


    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Сохраняем title_label как атрибут для последующего перевода
        self.title_label = QLabel(self.tr("Редактор расписания"))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        layout.addWidget(self.title_label)

        self.init_table()
        layout.addWidget(self.table)

        self.init_buttons(layout)
        self.setStyleSheet("background-color: #2C2C2C;")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.go_back_callback:
            self.go_back_callback()
            return
        super().keyPressEvent(event)

    def init_table(self):
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
        """)

        self.fill_table()
        self.table.cellDoubleClicked.connect(self.handle_double_click)

    def fill_table(self):
        from app.logic.schedule import get_full_schedule
        schedule_data = get_full_schedule()

        # Очистим текущие описания
        self.lesson_descriptions.clear()

        for col in range(1, self.num_slots + 1):
            item = QTableWidgetItem(f"{self.tr('Пара')} {col}")
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, col, item)

        for row in range(1, self.num_days + 1):
            item = QTableWidgetItem(self.days[row - 1])
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)

        for row in range(1, self.num_days + 1):
            for col in range(1, self.num_slots + 1):
                # Ищем соответствующую запись из БД
                record = next(
                    (item for item in schedule_data if item["day"] == self.days[row - 1] and item["time_slot"] == col),
                    None)
                subject = record["subject"] if record else ""
                topic = record["topic"] if record else ""

                item = QTableWidgetItem(subject)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

                # Сохраняем тему в lesson_descriptions
                if topic:
                    self.lesson_descriptions[(row, col)] = topic
                    # Можно добавить подсказку с темой
                    item.setToolTip(topic)
                    # Или выделить цветом
                    item.setBackground(QColor("#2E7D32"))
                else:
                    item.setToolTip("")
                    item.setBackground(QColor("#1E1E1E"))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 150)

        self.table.setColumnWidth(0, 150)

    def init_buttons(self, layout):
        buttons_container = QWidget()
        buttons_container.setStyleSheet("background: transparent;")
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(30)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Сохраняем кнопки как атрибуты для перевода
        self.btn_save = QPushButton(self.tr("Сохранить"))
        self.btn_save.setFixedSize(160, 50)
        self.btn_save.setStyleSheet("""
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
        self.btn_save.clicked.connect(self.on_save_clicked)
        buttons_layout.addWidget(self.btn_save)

        self.btn_back = QPushButton(self.tr("Назад"))
        self.btn_back.setFixedSize(160, 50)
        self.btn_back.setStyleSheet("""
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
        self.btn_back.clicked.connect(self.go_back_callback)
        buttons_layout.addWidget(self.btn_back)

        self.btn_clear = QPushButton(self.tr("Очистить"))
        self.btn_clear.setFixedSize(160, 50)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border-radius: 10px;
            }
        """)
        self.btn_clear.clicked.connect(self.clear_schedule)
        buttons_layout.addWidget(self.btn_clear)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(buttons_container)

    def clear_schedule(self):
        try:
            from app.logic.schedule import clear_schedule
            clear_schedule()

            for row in range(1, self.num_days + 1):
                for col in range(1, self.num_slots + 1):
                    if item := self.table.item(row, col):
                        item.setText("")

            self.lesson_descriptions.clear()
            self.table.viewport().update()

            if self.schedule_view_ref:
                self.schedule_view_ref.refresh()

            QMessageBox.information(self, self.tr("Успех"), self.tr("Расписание полностью очищено!"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Ошибка очистки"), f"{self.tr('Ошибка')}: {str(e)}")

    def handle_double_click(self, row, col):
        if row > 0 and col > 0:
            self.edit_lesson_description(row, col)

    def edit_lesson_description(self, row, col):
        current_description = self.lesson_descriptions.get((row, col), "")
        subject_item = self.table.item(row, col)
        subject = subject_item.text() if subject_item else ""

        dialog = QDialog(self)
        dialog.setWindowTitle(f"{self.tr('Описание пары')}: {subject}")
        dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText(current_description)
        text_edit.setFocus()

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
                subject_item.setBackground(QColor("#2E7D32"))
            else:
                subject_item.setBackground(QColor("#1E1E1E"))

    def on_save_clicked(self):
        try:
            from app.logic.schedule import save_schedule_item

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

            QMessageBox.information(self, self.tr("Успех"), self.tr("Расписание сохранено!"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Ошибка"), f"{self.tr('Ошибка')}: {str(e)}")

    def retranslate_ui(self):
        # Обновляем язык
        # При необходимости можно принимать новый lang как аргумент, если хочешь
        # Здесь просто обновляем все переводы, исходя из self.lang

        self.setWindowTitle(self.tr("Редактор расписания"))
        self.fill_table()
        self.init_buttons(self.layout())

        self.days = [
            self.tr("Понедельник"), self.tr("Вторник"), self.tr("Среда"),
            self.tr("Четверг"), self.tr("Пятница"), self.tr("Суббота")
        ]

        # Обновляем заголовок окна
        self.title_label.setText(self.tr("Редактор расписания"))

        # Обновляем заголовки таблицы (дни недели и пары)
        for col in range(1, self.num_slots + 1):
            item = self.table.item(0, col)
            if item:
                item.setText(f"{self.tr('Пара')} {col}")

        for row in range(1, self.num_days + 1):
            item = self.table.item(row, 0)
            if item:
                item.setText(self.days[row - 1])

        # Обновляем кнопки
        self.btn_save.setText(self.tr("Сохранить"))
        self.btn_back.setText(self.tr("Назад"))
        self.btn_clear.setText(self.tr("Очистить"))
def set_language(self, lang):
    self.lang = lang
    self.retranslate_ui()