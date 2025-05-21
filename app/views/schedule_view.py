from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.logic.schedule import schedule_data

class ScheduleView(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback

        self.setMinimumSize(1000, 650)  # чуть больше
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(0)  # без отступов, чтобы линии были смежные

        # Время пар — 5 пар
        self.times = ["08:00–09:30", "09:40–11:10", "11:20–12:50", "13:40–15:10", "15:20–16:50"]

        # Дни недели — 5 дней
        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

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
            border-right: 2px solid black;
            border-bottom: 2px solid black;
            border-radius: 4px;
        """)
        if self.go_back_callback:
            btn_back.clicked.connect(self.go_back_callback)
        self.layout.addWidget(btn_back, 0, 0)

        # Времена пар
        for col, time in enumerate(self.times, start=1):
            lbl = QLabel(time)
            lbl.setFixedSize(160, 50)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("""
                font-weight: bold; font-size: 14px;
                border-right: 2px solid black;
                border-bottom: 2px solid black;
                background-color: #444444; color: white;
            """)
            self.layout.addWidget(lbl, 0, col)

        # Дни недели
        for row, day in enumerate(self.days, start=1):
            day_lbl = QLabel(day)
            day_lbl.setFixedSize(150, 70)
            day_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_lbl.setStyleSheet("""
                font-weight: bold; font-size: 18px;
                border-right: 2px solid black;
                border-bottom: 2px solid black;
                background-color: #555555; color: white;
            """)
            self.layout.addWidget(day_lbl, row, 0)

            # Заполнение ячеек расписанием из schedule_data
            lessons = schedule_data.get(day, [])
            for col in range(1, len(self.times) + 1):
                if col - 1 < len(lessons):
                    subject, topic = lessons[col - 1]
                    text = f"<b>{subject}</b><br><small>{topic}</small>" if subject else ""
                else:
                    text = ""

                cell = QLabel(text)
                cell.setFixedSize(160, 70)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet("""
                    border-right: 2px solid black;
                    border-bottom: 2px solid black;
                """)
                cell.setWordWrap(True)
                self.layout.addWidget(cell, row, col)
