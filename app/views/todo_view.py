from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLineEdit, QPushButton, QListWidgetItem, QCheckBox,
    QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from app.logic.todo import get_all_tasks, add_task, toggle_task, delete_task


class TodoView(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

        # Контейнер ввода
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        # Поле ввода
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите новую задачу...")
        self.task_input.setMinimumHeight(50)
        self.task_input.setFont(QFont('Arial', 12))
        input_layout.addWidget(self.task_input, 4)

        # Кнопка добавления
        self.add_btn = QPushButton("Добавить")
        self.add_btn.setMinimumHeight(50)
        self.add_btn.setMinimumWidth(120)
        self.add_btn.setFont(QFont('Arial', 12, QFont.Bold))
        input_layout.addWidget(self.add_btn, 1)
        self.add_btn.clicked.connect(self.add_new_task)


        self.layout.addWidget(input_container)

        # Список задач
        self.tasks_list = QListWidget()
        self.tasks_list.setSpacing(10)
        self.layout.addWidget(self.tasks_list, 1)

        # Кнопка назад
        if self.go_back_callback:
            self.back_btn = QPushButton("← Назад")
            self.back_btn.setMinimumHeight(50)
            self.back_btn.setFont(QFont('Arial', 12))
            self.back_btn.clicked.connect(self.go_back_callback)
            self.layout.addWidget(self.back_btn)

    def setup_styles(self):
        self.setStyleSheet("""
            /* Основной фон */
            QWidget {
                background-color: #252525;
            }

            /* Поле ввода */
            QLineEdit {
                font-size: 16px;
                padding: 12px 15px;
                border: 2px solid #3F51B5;
                border-radius: 8px;
                background-color: #333;
                color: #FFF;
            }

            QLineEdit:focus {
                border-color: #5C6BC0;
            }

            /* Основные кнопки */
            QPushButton {
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                color: white;
            }

            #add_btn {
                background-color: #4CAF50;
            }

            #add_btn:hover {
                background-color: #66BB6A;
            }

            #back_btn {
                background-color: #E53935;
            }

            #back_btn:hover {
                background-color: #EF5350;
            }

            /* Список задач */
            QListWidget {
                background-color: #333;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 5px;
            }

            /* Карточка задачи */
            .TaskCard {
                background-color: #383838;
                border-radius: 8px;
                padding: 15px;
                border-left: 5px solid #3F51B5;
            }

            .TaskCard[priority="high"] {
                border-left-color: #EF5350;
            }

            /* Чекбокс */
            QCheckBox {
                spacing: 15px;
            }

            QCheckBox::indicator {
                width: 28px;
                height: 28px;
                border: 2px solid #5C6BC0;
                border-radius: 14px;
            }

            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }

            /* Текст задачи */
            .TaskLabel {
                color: #FFF;
                font-size: 16px;
                padding: 5px;
            }

            .TaskLabel[completed="true"] {
                color: #AAA;
                text-decoration: line-through;
            }

            /* Кнопка удаления */
            .DeleteBtn {
                background-color: #F44336;
                font-size: 14px;
                padding: 8px 15px;
                min-width: 90px;
            }

            .DeleteBtn:hover {
                background-color: #D32F2F;
            }
        """)

        self.add_btn.setObjectName("add_btn")
        if hasattr(self, 'back_btn'):
            self.back_btn.setObjectName("back_btn")

    def add_new_task(self):
        text = self.task_input.text().strip()
        if text:
            add_task(text)
            self.task_input.clear()
            self.load_tasks()


    def load_tasks(self):
        self.tasks_list.clear()
        for task in get_all_tasks():
            self.add_task_card(task)

    def add_task_card(self, task):
        item = QListWidgetItem()
        item.setSizeHint(QSize(-1, 80))  # Начальная высота (может увеличиться)

        card = QFrame()
        card.setObjectName("TaskCard")
        if task.get('priority') == 'high':
            card.setProperty("priority", "high")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(20)

        checkbox = QCheckBox()
        checkbox.setChecked(task.get('completed', False))
        checkbox.stateChanged.connect(
            lambda state, id=task['id']: self.toggle_task(id, checkbox)
        )
        layout.addWidget(checkbox)

        label = QLabel(task.get('task', 'Новая задача'))
        label.setObjectName("TaskLabel")
        label.setProperty("completed", "true" if task.get('completed') else "false")
        label.setWordWrap(True)  # Разрешаем перенос слов
        label.setFont(QFont('Arial', 14))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Растягиваем по вертикали
        layout.addWidget(label, 1)

        delete_btn = QPushButton("Удалить")
        delete_btn.setObjectName("DeleteBtn")
        delete_btn.clicked.connect(lambda _, id=task['id']: self.delete_task(id))
        layout.addWidget(delete_btn)

        self.tasks_list.addItem(item)
        self.tasks_list.setItemWidget(item, card)

        # Динамически подстраиваем высоту под содержимое
        height = label.sizeHint().height() + 30  # + отступы
        card.adjustSize()
        item.setSizeHint(card.sizeHint())

    def toggle_task(self, task_id, checkbox):
        toggle_task(task_id)
        # Обновляем стиль текста
        for i in range(self.tasks_list.count()):
            item = self.tasks_list.item(i)
            widget = self.tasks_list.itemWidget(item)
            if widget:
                label = widget.findChild(QLabel, "TaskLabel")  # исправлено
                if label:
                    label.setProperty("completed", "true" if checkbox.isChecked() else "false")
                    label.style().unpolish(label)
                    label.style().polish(label)

    def delete_task(self, task_id):
        delete_task(task_id)
        self.load_tasks()

    def showEvent(self, event):
        self.load_tasks()
        super().showEvent(event)