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

        self.times = [
            "08:00–09:30", "09:40–11:10", "11:20–12:50",
            "13:40–15:10", "15:20–16:50"
        ]
        self.days = [
            "Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"
        ]

        self._build_ui()

    def _build_ui(self):
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

        # Заголовки временных слотов
        for col, time in enumerate(self.times, start=1):
            lbl = QLabel(time)
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
        schedule_data = get_full_schedule()
        schedule_map = {
            (item["day"], item["time_slot"]): item["subject"]
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

            for col in range(1, len(self.times) + 1):
                subject = schedule_map.get((day, col), "")
                cell = QLabel(subject)
                cell.setMinimumSize(120, 60)
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet("""
                    font-size: 14px;
                    background-color: #444444;
                    color: white;
                    border-radius: 6px;
                """)
                self.layout.addWidget(cell, row, col)
