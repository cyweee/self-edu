from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLineEdit, QPushButton, QListWidgetItem, QCheckBox,
    QLabel, QFrame, QSizePolicy, QMenu
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from app.logic.todo import get_all_tasks, add_task, toggle_task, delete_task
from app.logic.language import translations


class TodoView(QWidget):
    def __init__(self, go_back_callback=None, lang = "ru"):
        super().__init__()
        self.lang = lang
        self.go_back_callback = go_back_callback
        self.setup_ui()
        self.setup_styles()
        self.selected_priority = "low"

    def tr(self, key):
        return translations.get(self.lang, {}).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.retranslate_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText(self.tr("Введите новую задачу..."))
        self.task_input.setMinimumHeight(50)
        self.task_input.setFont(QFont('Arial', 12))
        input_layout.addWidget(self.task_input, 4)

        # Кнопка выбора приоритета
        self.priority_btn = QPushButton("⋮")
        self.priority_btn.setMinimumSize(50, 50)
        self.priority_btn.setFont(QFont("Arial", 18))
        input_layout.addWidget(self.priority_btn)

        # Выпадающее меню с приоритетами
        priority_menu = QMenu(self)
        for label, color, level in [
            (self.tr("Высокий"), "#e02f56", "high"),
            (self.tr("Средний"), "#e67a00", "medium"),
            (self.tr("Низкий"), "#05eb92", "low"),
        ]:
            action = priority_menu.addAction(label)
            action.setData((level, color))
        priority_menu.triggered.connect(self.set_priority)
        self.priority_btn.setMenu(priority_menu)

        # Кнопка "Добавить"
        self.add_btn = QPushButton(self.tr("Добавить"))
        self.add_btn.setMinimumHeight(50)
        self.add_btn.setMinimumWidth(120)
        self.add_btn.setFont(QFont('Arial', 12, QFont.Bold))
        input_layout.addWidget(self.add_btn, 1)
        self.add_btn.clicked.connect(self.add_new_task)

        self.layout.addWidget(input_container)

        self.tasks_list = QListWidget()
        self.tasks_list.setSpacing(10)
        self.layout.addWidget(self.tasks_list, 1)

        if self.go_back_callback:
            self.back_btn = QPushButton(f"← {self.tr('Назад')}")
            self.back_btn.setMinimumHeight(50)
            self.back_btn.setFont(QFont('Arial', 12))
            self.back_btn.clicked.connect(self.go_back_callback)
            self.layout.addWidget(self.back_btn)

    def set_priority(self, action):
        level, color = action.data()
        self.selected_priority = level
        self.priority_btn.setStyleSheet(f"background-color: {color}; color: white;")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.go_back_callback:
            self.go_back_callback()
            return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.task_input.hasFocus():
                self.add_new_task()
                return
        super().keyPressEvent(event)

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #252525;
            }
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
            QListWidget {
                background-color: #333;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
            .TaskCard {
                background-color: #383838;
                border-radius: 8px;
                padding: 15px;
                border-left: 5px solid #3F51B5;
            }
            .TaskCard[priority="high"] {
                border-left-color: #EF5350;
            }
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
            .TaskLabel {
                color: #FFF;
                font-size: 16px;
                padding: 5px;
            }
            .TaskLabel[completed="true"] {
                color: #AAA;
                text-decoration: line-through;
            }
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
            add_task(text, priority=self.selected_priority)
            self.task_input.clear()
            self.selected_priority = "low"
            self.priority_btn.setStyleSheet("")  # сброс цвета
            self.load_tasks()


    def load_tasks(self):
        self.tasks_list.clear()
        for task in get_all_tasks():
            self.add_task_card(task)

    def add_task_card(self, task):
        item = QListWidgetItem()
        item.setSizeHint(QSize(-1, 80))

        card = QFrame()  # СНАЧАЛА создаём card
        card.setObjectName("TaskCard")

        # Устанавливаем приоритет и стили
        priority = task.get('priority')
        if priority == 'high':
            card.setProperty("priority", "high")
        elif priority == 'medium':
            card.setStyleSheet("border-left: 5px solid #e67a00;")
        elif priority == 'low':
            card.setStyleSheet("border-left: 5px solid #05eb92;")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(20)

        checkbox = QCheckBox()
        checkbox.setChecked(task.get('completed', False))
        checkbox.stateChanged.connect(
            lambda state, id=task['id']: self.toggle_task(id, checkbox)
        )
        layout.addWidget(checkbox)

        label = QLabel(task.get('task', self.tr('Новая задача')))
        label.setObjectName("TaskLabel")
        label.setProperty("completed", "true" if task.get('completed') else "false")
        label.setWordWrap(True)
        label.setFont(QFont('Arial', 14))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(label, 1)

        delete_btn = QPushButton(self.tr("Удалить"))
        delete_btn.setObjectName("DeleteBtn")
        delete_btn.clicked.connect(lambda _, id=task['id']: self.delete_task(id))
        layout.addWidget(delete_btn)

        self.tasks_list.addItem(item)
        self.tasks_list.setItemWidget(item, card)

        card.adjustSize()
        item.setSizeHint(card.sizeHint())

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

        label = QLabel(task.get('task', self.tr('Новая задача')))
        label.setObjectName("TaskLabel")
        label.setProperty("completed", "true" if task.get('completed') else "false")
        label.setWordWrap(True)
        label.setFont(QFont('Arial', 14))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(label, 1)

        delete_btn = QPushButton(self.tr("Удалить"))
        delete_btn.setObjectName("DeleteBtn")
        delete_btn.clicked.connect(lambda _, id=task['id']: self.delete_task(id))
        layout.addWidget(delete_btn)

        self.tasks_list.addItem(item)
        self.tasks_list.setItemWidget(item, card)

        card.adjustSize()
        item.setSizeHint(card.sizeHint())

    def toggle_task(self, task_id, checkbox):
        toggle_task(task_id)
        for i in range(self.tasks_list.count()):
            item = self.tasks_list.item(i)
            widget = self.tasks_list.itemWidget(item)
            if widget:
                label = widget.findChild(QLabel, "TaskLabel")
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

    def retranslate_ui(self):
        self.task_input.setPlaceholderText(self.tr("Введите новую задачу..."))
        self.add_btn.setText(self.tr("Добавить"))
        self.fill_table()
        self.init_buttons(self.layout())

        if self.go_back_callback and hasattr(self, "back_btn"):
            self.back_btn.setText(f"← {self.tr('Назад')}")

        # После смены языка нужно перезагрузить задачи,
        # чтобы перевести текст "Новая задача" в add_task_card, если он встречается
        self.load_tasks()