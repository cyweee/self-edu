from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLineEdit, QPushButton, QListWidgetItem, QCheckBox,
    QLabel
)
from PySide6.QtCore import Qt
from app.logic.todo import get_all_tasks, add_task, toggle_task, delete_task

class TodoView(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Поле ввода новой задачи
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите новую задачу...")
        self.task_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
        """)
        self.layout.addWidget(self.task_input)

        # Кнопка добавления
        add_btn = QPushButton("Добавить")
        add_btn.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        """)
        add_btn.clicked.connect(self.add_new_task)
        self.layout.addWidget(add_btn)

        # Список задач
        self.tasks_list = QListWidget()
        self.tasks_list.setStyleSheet("""
            font-size: 16px;
            background-color: #333;
            color: white;
            border-radius: 8px;
        """)
        self.layout.addWidget(self.tasks_list)

        # Кнопка "Назад"
        if self.go_back_callback:
            back_btn = QPushButton("← Назад")
            back_btn.setStyleSheet("""
                font-size: 16px;
                padding: 10px;
                background-color: #E53935;
                color: white;
                border-radius: 8px;
            """)
            back_btn.clicked.connect(self.go_back_callback)
            self.layout.addWidget(back_btn)

        self.load_tasks()

    def load_tasks(self):
        self.tasks_list.clear()
        for task in get_all_tasks():
            item = QListWidgetItem()
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(5, 5, 5, 5)

            # Чекбокс
            checkbox = QCheckBox()
            checkbox.setChecked(task['completed'])
            checkbox.stateChanged.connect(
                lambda state, id=task['id']: toggle_task(id)
            )

            # Текст задачи
            label = QLabel(task['task'])
            label.setStyleSheet("color: white; font-size: 16px;")
            label.setWordWrap(True)

            # Кнопка удаления
            delete_btn = QPushButton("×")
            delete_btn.setStyleSheet("""
                color: white;
                background-color: #F44336;
                border-radius: 10px;
                font-weight: bold;
            """)
            delete_btn.setFixedSize(30, 30)
            delete_btn.clicked.connect(
                lambda _, id=task['id']: self.delete_task(id)
            )

            layout.addWidget(checkbox)
            layout.addWidget(label)
            layout.addWidget(delete_btn)
            item.setSizeHint(widget.sizeHint())
            self.tasks_list.addItem(item)
            self.tasks_list.setItemWidget(item, widget)

    def add_new_task(self):
        text = self.task_input.text().strip()
        if text:
            add_task(text)
            self.task_input.clear()
            self.load_tasks()

    def delete_task(self, task_id):
        delete_task(task_id)
        self.load_tasks()

    def showEvent(self, event):
        self.load_tasks()
        super().showEvent(event)