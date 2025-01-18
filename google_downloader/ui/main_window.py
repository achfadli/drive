import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QVBoxLayout, QTabWidget, QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

# Import tab widgets
from google_downloader.ui.download_tab import DownloadTab
from google_downloader.ui.history_tab import HistoryTab
from google_downloader.ui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Konfigurasi jendela utama
        self.setWindowTitle("Google Drive Downloader")
        self.setGeometry(100, 100, 900, 600)

        # Coba set icon (pastikan path benar)
        try:
            # Sesuaikan path icon jika perlu
            icon_path = 'resources/icons/download_icon.png'
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            QMessageBox.warning(self, "Peringatan", f"Gagal memuat ikon: {e}")

        # Widget pusat
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Tab Widget
        self.tab_widget = QTabWidget()

        # Tambah Tab
        self.download_tab = DownloadTab()
        self.history_tab = HistoryTab()
        self.settings_tab = SettingsTab()

        self.tab_widget.addTab(self.download_tab, "Download")
        self.tab_widget.addTab(self.history_tab, "Riwayat")
        self.tab_widget.addTab(self.settings_tab, "Pengaturan")

        main_layout.addWidget(self.tab_widget)
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        # Styling
        self.setup_styles()

    def setup_styles(self):
        """Mengatur gaya visual aplikasi"""
        self.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QTabWidget::pane {
            border: 1px solid #d3d3d3;
            background: white;
        }
        QTabBar::tab {
            background: #e0e0e0;
            color: black;
            padding: 10px;
            min-width: 100px;
            font-weight: bold;
        }
        QTabBar::tab:selected {
            background: #3498db;
            color: white;
        }
        QTabBar::tab:hover {
            background: #2980b9;
            color: white;
        }
        """)

    def closeEvent(self, event):
        """
        Tangani event penutupan aplikasi
        Tambahkan konfirmasi sebelum keluar
        """
        reply = QMessageBox.question(
            self,
            'Konfirmasi Keluar',
            'Apakah Anda yakin ingin keluar?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def create_main_window():
    """
    Fungsi untuk membuat instance MainWindow

    Returns:
        MainWindow: Instance window utama
    """
    return MainWindow()


def run_application():
    """
    Fungsi untuk menjalankan aplikasi
    """
    # Pastikan hanya satu instance QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Buat dan tampilkan window
    window = create_main_window()
    window.show()

    # Jalankan event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    run_application()