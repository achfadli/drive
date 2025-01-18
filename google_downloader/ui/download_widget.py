from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit,
    QProgressBar, QFileDialog, QLabel
)
from PySide6.QtCore import Qt, QThread, Signal
from core.downloader import Downloader


class DownloadWorker(QThread):
    progress_update = Signal(int)
    download_complete = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, url, output_dir):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.downloader = Downloader(output_dir)

    def run(self):
        try:
            # Logika download sesuaikan dengan jenis URL
            if 'drive.google.com' in self.url:
                result = self.downloader.download_google_drive(self.url)
            elif 'docs.google.com' in self.url:
                result = self.downloader.download_google_docs(self.url)
            else:
                self.error_occurred.emit("URL tidak didukung")
                return

            if result:
                self.download_complete.emit("Download Berhasil!")
            else:
                self.error_occurred.emit("Download Gagal")
        except Exception as e:
            self.error_occurred.emit(str(e))


class DownloadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # URL Input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL Google Drive/Docs")
        url_layout.addWidget(self.url_input)

        # Tombol Pilih Folder
        self.folder_button = QPushButton("Pilih Folder")
        self.folder_button.clicked.connect(self.pilih_folder)
        url_layout.addWidget(self.folder_button)

        # Tombol Download
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.mulai_download)
        url_layout.addWidget(self.download_button)

        layout.addLayout(url_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Log Area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

        # Default output directory
        self.output_dir = "./downloads"

    def pilih_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Pilih Folder Download")
        if folder:
            self.output_dir = folder
            self.log_tambah(f"Folder dipilih: {folder}")

    def mulai_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.log_tambah("Masukkan URL terlebih dahulu")
            return

        # Reset progress
        self.progress_bar.setValue(0)

        # Inisiasi download worker
        self.download_worker = DownloadWorker(url, self.output_dir)
        self.download_worker.progress_update.connect(self.update_progress)
        self.download_worker.download_complete.connect(self.download_selesai)
        self.download_worker.error_occurred.connect(self.download_error)

        self.download_worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_selesai(self, message):
        self.log_tambah(message)
        self.progress_bar.setValue(100)

    def download_error(self, error):
        self.log_tambah(f"Error: {error}")

    def log_tambah(self, pesan):
        self.log_area.append(pesan)