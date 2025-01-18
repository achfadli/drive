from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit,
    QProgressBar, QLabel, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal
from google_downloader.core.downloader import Downloader
from google_downloader.utils.logger import Logger


class DownloadWorker(QThread):
    progress_update = Signal(int)
    download_complete = Signal(str)
    download_error = Signal(str)

    def __init__(self, url, output_dir):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.downloader = Downloader(output_dir)
        self.logger = Logger()

    def run(self):
        try:
            result = self.downloader.download(self.url)
            if result:
                self.download_complete.emit(f"Download berhasil: {result}")
                self.logger.log_success(f"Download berhasil: {result}")
            else:
                self.download_error.emit("Download gagal")
                self.logger.log_error("Download gagal")
        except Exception as e:
            self.download_error.emit(str(e))
            self.logger.log_error(f"Error download: {e}")


class DownloadTab(QWidget):
    def __init__(self):
        super().__init__()
        self.output_dir = "./downloads"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # URL Input Section
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

    def pilih_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Pilih Folder Download")
        if folder:
            self.output_dir = folder
            self.log_tambah(f"Folder download: {folder}")

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
        self.download_worker.download_error.connect(self.download_error)

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