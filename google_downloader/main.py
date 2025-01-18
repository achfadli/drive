import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    # Pastikan hanya satu instance QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Buat dan tampilkan window
    window = MainWindow()
    window.show()

    # Jalankan event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()