from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QLineEdit, QPushButton, QListWidgetItem, QLabel,
    QFrame, QComboBox
)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QFont, QDesktopServices
from app.logic.useful_links import get_all_links, add_link, delete_link
from app.logic.language import translations


class UsefulLinksView(QWidget):
    def __init__(self, go_back_callback=None, lang = "ru"):
        super().__init__()
        self.lang = lang
        self.go_back_callback = go_back_callback
        self.setup_ui()
        self.setup_styles()
        self.load_links()

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

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(self.tr("Название ссылки"))
        self.title_input.setMinimumHeight(50)
        input_layout.addWidget(self.title_input, 2)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(self.tr("URL (https://...)"))
        self.url_input.setMinimumHeight(50)
        input_layout.addWidget(self.url_input, 3)

        self.category_input = QComboBox()
        self.category_items = [
            "Программирование",
            "Математика",
            "Физика",
            "Комп.Сети",
            "Англ язык",
            "Чешский язык",
            "Другое"
        ]
        self.category_input.addItems([self.tr(cat) for cat in self.category_items])
        self.category_input.setMinimumHeight(50)
        input_layout.addWidget(self.category_input, 1)

        self.add_btn = QPushButton(self.tr("Добавить"))
        self.add_btn.setMinimumHeight(50)
        self.add_btn.setMinimumWidth(120)
        self.add_btn.clicked.connect(self.add_new_link)
        input_layout.addWidget(self.add_btn)

        self.layout.addWidget(input_container)

        self.links_list = QListWidget()
        self.links_list.setSpacing(10)
        self.layout.addWidget(self.links_list, 1)

        if self.go_back_callback:
            self.back_btn = QPushButton(f"← {self.tr('Назад')}")
            self.back_btn.setMinimumHeight(50)
            self.back_btn.clicked.connect(self.go_back_callback)
            self.layout.addWidget(self.back_btn)

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #252525;
            }
            QLineEdit, QComboBox {
                font-size: 16px;
                padding: 12px;
                border: 2px solid #3F51B5;
                border-radius: 8px;
                background-color: #333;
                color: #FFF;
            }
            QPushButton {
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                color: white;
                background-color: #3F51B5;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
            QListWidget {
                background-color: #333;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
            .LinkCard {
                background-color: #383838;
                border-radius: 8px;
                padding: 15px;
            }
            .LinkTitle {
                color: #FFF;
                font-size: 16px;
                font-weight: bold;
            }
            .LinkUrl {
                color: #AAA;
                font-size: 14px;
            }
            .LinkCategory {
                color: #5C6BC0;
                font-size: 14px;
                font-style: italic;
            }
            .DeleteBtn {
                background-color: #F44336;
            }
        """)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.go_back_callback:
            self.go_back_callback()
            return

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if any([
                self.title_input.hasFocus(),
                self.url_input.hasFocus(),
                self.category_input.hasFocus()
            ]):
                self.add_new_link()
                return

        super().keyPressEvent(event)

    def load_links(self):
        self.links_list.clear()
        for link in get_all_links():
            self.add_link_card(link)

    def add_link_card(self, link):
        item = QListWidgetItem()

        card = QFrame()
        card.setObjectName("LinkCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)

        title_layout = QHBoxLayout()

        title = QLabel(link['title'])
        title.setObjectName("LinkTitle")
        title.setWordWrap(True)
        title_layout.addWidget(title, 1)

        category = QLabel(link['category'])
        category.setObjectName("LinkCategory")
        title_layout.addWidget(category)

        layout.addLayout(title_layout)

        url = QLabel(link['url'])
        url.setObjectName("LinkUrl")
        url.setTextInteractionFlags(Qt.TextBrowserInteraction)
        url.setOpenExternalLinks(True)
        url.setWordWrap(True)
        layout.addWidget(url)

        btn_layout = QHBoxLayout()

        open_btn = QPushButton(self.tr("Открыть"))
        open_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link['url'])))
        btn_layout.addWidget(open_btn)

        delete_btn = QPushButton(self.tr("Удалить"))
        delete_btn.setObjectName("DeleteBtn")
        delete_btn.clicked.connect(lambda: self.delete_link(link['id']))
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        card.adjustSize()
        item.setSizeHint(card.sizeHint())
        self.links_list.addItem(item)
        self.links_list.setItemWidget(item, card)

    def add_new_link(self):
        title = self.title_input.text().strip()
        url = self.url_input.text().strip()
        category = self.category_input.currentText()

        if title and url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            add_link(title, url, category)
            self.title_input.clear()
            self.url_input.clear()
            self.load_links()

    def delete_link(self, link_id):
        delete_link(link_id)
        self.load_links()

    def showEvent(self, event):
        self.load_links()
        super().showEvent(event)

    def retranslate_ui(self):
        self.title_input.setPlaceholderText(self.tr("Название ссылки"))
        self.url_input.setPlaceholderText(self.tr("URL (https://...)"))
        self.fill_table()
        self.init_buttons(self.layout())

        # Обновляем список категорий с переводом
        current_category = self.category_input.currentText()
        self.category_input.clear()
        self.category_input.addItems([self.tr(cat) for cat in self.category_items])
        # Если категория была выбрана, пытаемся вернуть выбор по тексту
        index = self.category_input.findText(current_category)
        if index >= 0:
            self.category_input.setCurrentIndex(index)

        self.add_btn.setText(self.tr("Добавить"))

        if self.go_back_callback and hasattr(self, "back_btn"):
            self.back_btn.setText(f"← {self.tr('Назад')}")

        # Сохраняем текущую выбранную категорию
        current_category = self.category_input.currentText()
        translated_categories = [self.tr(cat) for cat in self.category_items]

        # Обновляем комбобокс
        self.category_input.clear()
        self.category_input.addItems(translated_categories)

        # Восстанавливаем выбранную категорию
        if current_category in translated_categories:
            self.category_input.setCurrentText(current_category)

        # Обновляем кнопки "Открыть" и "Удалить" в карточках ссылок — проще просто перезагрузить список
        self.load_links()