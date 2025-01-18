from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from google_downloader.utils.helpers import Helpers
import os


class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.download_dir = "./downloads"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tabel Riwayat Download
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nama File", "Ukuran", "Lokasi", "Aksi"])

        # Atur lebar kolom
        self.table.setColumnWidth(0, 250)  # Nama File
        self.table.setColumnWidth(1, 100)  # Ukuran
        self.table.setColumnWidth(2, 300)  # Lokasi
        self.table.setColumnWidth(3, 100)  # Aksi

        # Aktifkan seleksi baris penuh
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Tombol Refresh
        refresh_button = QPushButton("Refresh Riwayat")
        refresh_button.clicked.connect(self.load_download_history)
        refresh_button.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 10px;
        """)

        layout.addWidget(self.table)
        layout.addWidget(refresh_button)

        self.setLayout(layout)

        # Muat riwayat download saat inisialisasi
        self.load_download_history()

    def load_download_history(self):
        """Memuat riwayat download"""
        # Bersihkan tabel
        self.table.setRowCount(0)

        try:
            # Pastikan direktori download ada
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)

            # Dapatkan daftar file
            files = os.listdir(self.download_dir)

            # Isi tabel
            for file in files:
                file_path = os.path.join(self.download_dir, file)

                # Cek apakah benar-benar file
                if os.path.isfile(file_path):
                    # Tambah baris baru
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Nama File
                    self.table.setItem(row_position, 0, QTableWidgetItem(file))

                    # Ukuran File
                    file_size = Helpers.get_file_size(file_path)
                    size_text = f"{file_size / 1024:.2f} KB" if file_size else "N/A"
                    self.table.setItem(row_position, 1, QTableWidgetItem(size_text))

                    # Lokasi File
                    self.table.setItem(row_position, 2, QTableWidgetItem(file_path))

                    # Tombol Aksi (Buka File)
                    open_button = QPushButton("Buka")
                    open_button.clicked.connect(lambda checked, path=file_path: self.buka_file(path))
                    self.table.setCellWidget(row_position, 3, open_button)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal memuat riwayat: {str(e)}")

    def buka_file(self, file_path):
        """Membuka file"""
        try:
            if Helpers.open_file(file_path):
                QMessageBox.information(self, "Sukses", f"Membuka file: {file_path}")
            else:
                QMessageBox.warning(self, "Error", f"Gagal membuka file: {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal membuka file: {str(e)}")