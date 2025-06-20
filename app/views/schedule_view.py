from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.logic.schedule import get_full_schedule
from app.logic.language import translations


class ScheduleView(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.lang = "en"
        self.go_back_callback = go_back_callback

        self.setMinimumSize(1200, 750)
        self.setStyleSheet("background-color: #2C2C2C;")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setHorizontalSpacing(10)
        self.layout.setVerticalSpacing(10)

        self.days_keys = [
            "Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"
        ]
        self.days = [self.tr(day) for day in self.days_keys]

        self.num_slots = 5
        self.num_days = len(self.days)
        self.schedule_data = []

        self.back_btn = None  # ссылка на кнопку назад
        self._build_ui()

    def tr(self, key):
        return translations.get(self.lang, {}).get(key, key)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.go_back_callback:
            self.go_back_callback()
            return
        super().keyPressEvent(event)

    def refresh(self):
        # очищаем все виджеты
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self._build_ui()

    def showEvent(self, event):
        self._build_ui()
        super().showEvent(event)

    def _build_ui(self):
        # очищаем перед построением
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # обновляем дни с переводом
        self.days = [self.tr(day) for day in self.days_keys]

        schedule_data = get_full_schedule()
        schedule_map = {
            (item["day"], item["time_slot"]): (item["subject"], item["topic"])
            for item in schedule_data
        }

        # Заголовки столбцов — пары
        for col in range(1, self.num_slots + 1):
            lbl = QLabel(f"{self.tr('Пара')} {col}")
            lbl.setMinimumSize(120, 50)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("""
                font-weight: bold;
                font-size: 14px;
                background-color: #3F51B5;
                color: white;
                border-radius: 6px;
            """)
            self.layout.addWidget(lbl, 0, col)

        # Заголовки строк — дни недели и ячейки
        for row, day in enumerate(self.days, start=1):
            day_lbl = QLabel(day)
            day_lbl.setMinimumSize(150, 60)
            day_lbl.setAlignment(Qt.AlignCenter)
            day_lbl.setStyleSheet("""
                font-weight: bold;
                font-size: 16px;
                background-color: #3F51B5;
                color: white;
                border-radius: 6px;
            """)
            self.layout.addWidget(day_lbl, row, 0)

            for col in range(1, self.num_slots + 1):
                subject, topic = schedule_map.get((day, col), ("", ""))

                cell = QLabel(subject)
                cell.setMinimumSize(120, 60)
                cell.setAlignment(Qt.AlignCenter)

                if topic:
                    cell.setToolTip(f"{self.tr('Описание')}: {topic}")
                    cell.setStyleSheet("""
                        background-color: #3F51B5;
                        font-weight: bold;
                        border: 1px solid #7986CB;
                    """)
                else:
                    cell.setStyleSheet("""
                        background-color: #444444;
                        color: white;
                    """)

                self.layout.addWidget(cell, row, col)

        # Кнопка назад: создаем один раз
        if self.back_btn is None:
            self.back_btn = QPushButton()
            self.back_btn.setFixedSize(150, 50)
            self.back_btn.setStyleSheet("""
                font-weight: bold;
                font-size: 16px;
                background-color: #E53935;
                color: white;
                border-radius: 8px;
            """)
            if self.go_back_callback:
                self.back_btn.clicked.connect(self.go_back_callback)
            self.layout.addWidget(self.back_btn, 0, 0, 1, 1)

        self.back_btn.setText(f"← {self.tr('Назад')}")

    def retranslate_ui(self):
        # Обновляем переводы
        self.days = [self.tr(day) for day in self.days_keys]
        self._build_ui()
