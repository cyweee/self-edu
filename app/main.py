import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor



def apply_color_theme(app: QApplication):
    palette = QPalette()

    # Фон
    palette.setColor(QPalette.ColorRole.Window, QColor("#2C2C2C"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#1E1E1E"))

    # Текст
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))

    # Кнопки
    palette.setColor(QPalette.ColorRole.Button, QColor("#3F51B5"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))

    app.setPalette(palette)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Self-Education")

    apply_color_theme(app)

    from app.database.models import init_db
    init_db()

    from app.views.main_window import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()