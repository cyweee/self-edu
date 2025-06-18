from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.logic.schedule import get_full_schedule


class ScheduleView(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback

        self.setMinimumSize(1200, 750)
        self.setStyleSheet("background-color: #2C2C2C;")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setHorizontalSpacing(10)
        self.layout.setVerticalSpacing(10)

        # Убрали временные слоты, оставили только номера пар
        self.days = [
            "Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"
        ]

        self.num_slots = 5  # 5 пар в день
        self.num_days = len(self.days)    # 6 дней

        self.schedule_data = []

        self._build_ui()

    def keyPressEvent(self, event):
        # Только Esc - назад
        if event.key() == Qt.Key_Escape and self.go_back_callback:
            self.go_back_callback()
            return

        super().keyPressEvent(event)

    def refresh(self): #  перезагружает данные
        # 1. Очищаем текущий layout
        for i in reversed(range(self.layout.count())):
            if widget := self.layout.itemAt(i).widget():
                widget.deleteLater()

        # 2. Перестраиваем интерфейс
        self._build_ui()

    def showEvent(self, event):
        self._build_ui()  # Перестраиваем интерфейс при каждом открытии
        super().showEvent(event)

    def _build_ui(self):
        # Очищаем предыдущий layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        schedule_data = get_full_schedule()

        # Группировка данных по дням
        schedule_by_day = {}
        for item in schedule_data:
            day = item["day"]
            if day not in schedule_by_day:
                schedule_by_day[day] = {}
            schedule_by_day[day][item["time_slot"]] = item

        # Заголовки пар (просто номера)
        for col in range(1, self.num_slots + 1):
            lbl = QLabel(f"Пара {col}")
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

        # Заголовки дней и ячейки расписания
        schedule_map = {
            (item["day"], item["time_slot"]): (item["subject"], item["topic"])
            for item in schedule_data
        }

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
                    cell.setToolTip(f"Описание: {topic}")
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

        # Кнопка "Назад"
        btn_back = QPushButton("← Назад")
        btn_back.setFixedSize(150, 50)
        btn_back.setStyleSheet("""
            font-weight: bold;
            font-size: 16px;
            background-color: #E53935;
            color: white;
            border-radius: 8px;
        """)
        if self.go_back_callback:
            btn_back.clicked.connect(self.go_back_callback)
        self.layout.addWidget(btn_back, 0, 0, 1, 1)