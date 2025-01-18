from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QCheckBox,
    QPushButton, QLineEdit, QMessageBox,
    QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt
from utils.config import ConfigManager
from utils.helpers import Helpers


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.init_ui()
        self.load_current_settings()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Tema Pengaturan
        theme_group = QGroupBox("Pengaturan Tema")
        theme_layout = QFormLayout()

        # Pilih Tema
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_layout.addRow("Tema Aplikasi:", self.theme_combo)

        theme_group.setLayout(theme_layout)
        main_layout.addWidget(theme_group)

        # Pengaturan Download
        download_group = QGroupBox("Pengaturan Download")
        download_layout = QFormLayout()

        # Direktori Download Default
        self.download_dir_input = QLineEdit()
        download_dir_button = QPushButton("Pilih")
        download_dir_button.clicked.connect(self.pilih_direktori_download)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.download_dir_input)
        dir_layout.addWidget(download_dir_button)
        download_layout.addRow("Direktori Download:", dir_layout)

        # Opsi Tambahan
        self.auto_open_check = QCheckBox("Buka Folder Otomatis Setelah Download")
        download_layout.addRow(self.auto_open_check)

        self.max_download_check = QCheckBox("Batasi Kecepatan Download")
        download_layout.addRow(self.max_download_check)

        download_group.setLayout(download_layout)
        main_layout.addWidget(download_group)

        # Proxy Pengaturan
        proxy_group = QGroupBox("Pengaturan Proxy")
        proxy_layout = QFormLayout()

        self.use_proxy_check = QCheckBox("Gunakan Proxy")
        proxy_layout.addRow(self.use_proxy_check)

        self.proxy_url_input = QLineEdit()
        proxy_layout.addRow("Proxy URL:", self.proxy_url_input)

        self.proxy_port_input = QLineEdit()
        proxy_layout.addRow("Proxy Port:", self.proxy_port_input)

        proxy_group.setLayout(proxy_layout)
        main_layout.addWidget(proxy_group)

        # Tombol Simpan
        save_button = QPushButton("Simpan Pengaturan")
        save_button.clicked.connect(self.simpan_pengaturan)
        save_button.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            padding: 10px;
            font-weight: bold;
        """)
        main_layout.addWidget(save_button)

        # Tambah stretch untuk mengisi ruang kosong
        main_layout.addStretch()

        self.setLayout(main_layout)

    def load_current_settings(self):
        """Memuat pengaturan saat ini"""
        # Tema
        current_theme = self.config_manager.get('default_theme', 'Light')
        self.theme_combo.setCurrentText(current_theme)

        # Direktori Download
        download_dir = self.config_manager.get('download_directory', '')
        self.download_dir_input.setText(download_dir)

        # Opsi Download
        auto_open = self.config_manager.get('auto_open_folder', False)
        self.auto_open_check.setChecked(auto_open)

        # Pengaturan Proxy
        use_proxy = self.config_manager.get('proxy_settings', {}).get('use_proxy', False)
        self.use_proxy_check.setChecked(use_proxy)

        proxy_url = self.config_manager.get('proxy_settings', {}).get('proxy_url', '')
        self.proxy_url_input.setText(proxy_url)

        proxy_port = self.config_manager.get('proxy_settings', {}).get('proxy_port', '')
        self.proxy_port_input.setText(proxy_port)

    def pilih_direktori_download(self):
        """Memilih direktori download"""
        directory = Helpers.choose_directory()
        if directory:
            self.download_dir_input.setText(directory)

    def simpan_pengaturan(self):
        """Menyimpan pengaturan"""
        try:
            # Simpan tema
            theme = self.theme_combo.currentText()
            self.config_manager.set('default_theme', theme)

            # Simpan direktori download
            download_dir = self.download_dir_input.text()
            self.config_manager.set('download_directory', download_dir)

            # Simpan opsi download
            self.config_manager.set('auto_open_folder', self.auto_open_check.isChecked())

            # Simpan pengaturan proxy
            proxy_settings = {
                'use_proxy': self.use_proxy_check.isChecked(),
                'proxy_url': self.proxy_url_input.text(),
                'proxy_port': self.proxy_port_input.text()
            }
            self.config_manager.set('proxy_settings', proxy_settings)

            # Beri konfirmasi
            QMessageBox.information(
                self,
                "Pengaturan Tersimpan",
                "Pengaturan berhasil disimpan!"
            )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Kesalahan",
                f"Gagal menyimpan pengaturan: {str(e)}"
            )