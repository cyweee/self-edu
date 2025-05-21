from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt


class ScheduleEditorView(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()

        self.go_back_callback = go_back_callback
        self.setWindowTitle("Изменить расписание")
        self.resize(1000, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        title_label = QLabel("Редактор расписания")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        main_layout.addWidget(title_label)

        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])
        self.table.setVerticalHeaderLabels([
            "08:00-09:30", "09:40-11:10", "11:20–12:50",
            "13:40–15:10", "15:20–16:50"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1E1E1E;
                color: white;
                font-size: 16px;
                gridline-color: #3F51B5;
            }
            QHeaderView::section {
                background-color: #3F51B5;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
        """)

        main_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        btn_save = QPushButton("Сохранить")
        btn_save.setFixedSize(160, 50)
        btn_save.setStyleSheet("font-size: 18px; color: white; background-color: #3F51B5; border-radius: 10px;")
        btn_save.clicked.connect(self.save_schedule)
        button_layout.addWidget(btn_save)

        btn_back = QPushButton("Назад")
        btn_back.setFixedSize(160, 50)
        btn_back.setStyleSheet("font-size: 18px; color: white; background-color: #3F51B5; border-radius: 10px;")
        btn_back.clicked.connect(self.go_back_callback)
        button_layout.addWidget(btn_back)

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(button_layout)

        self.setStyleSheet("background-color: #2C2C2C;")

        # Вызов сразу для установки размеров при старте
        self.adjust_table_sizes()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_table_sizes()

    def adjust_table_sizes(self):
        # Размеры окна без отступов (границ, маргинов)
        available_width = self.width() - 80  # 40 слева + 40 справа margin
        available_height = self.height() - 160  # верхний + нижний отступы + место под кнопки

        # Число столбцов и строк
        cols = self.table.columnCount()
        rows = self.table.rowCount()

        # Пропорция ширины столбца к высоте строки (примерно 1.6)
        ratio = 1.6

        # Вычислим максимально возможную высоту строки и ширину столбца с учётом пропорции
        max_row_height = available_height / rows
        max_col_width = available_width / cols

        # Чтобы сохранить пропорции: ширина = ratio * высота
        # Проверим, какой из вариантов меньше и выберем его
        if max_col_width / max_row_height > ratio:
            # Ограничиваем ширину по высоте
            row_height = max_row_height
            col_width = int(row_height * ratio)
        else:
            # Ограничиваем высоту по ширине
            col_width = max_col_width
            row_height = int(col_width / ratio)

        # Устанавливаем размеры ячеек
        for row in range(rows):
            self.table.setRowHeight(row, int(row_height))
        for col in range(cols):
            self.table.setColumnWidth(col, int(col_width))

    def save_schedule(self):
        print("Сохраняем расписание...")
        # TODO: логика сохранения
        pass
