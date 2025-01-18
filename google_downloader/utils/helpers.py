import os
import platform
import string
import subprocess
from typing import Optional


class Helpers:
    @staticmethod
    def open_file(file_path: str) -> bool:
        """
        Membuka file sesuai sistem operasi

        Args:
            file_path (str): Path file yang akan dibuka

        Returns:
            bool: Status pembukaan file
        """
        try:
            if not os.path.exists(file_path):
                print(f"File tidak ditemukan: {file_path}")
                return False

            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(file_path)
            elif platform.system() == 'Linux':  # Linux
                subprocess.call(('xdg-open', file_path))
            else:
                print("Sistem operasi tidak didukung")
                return False

            return True
        except Exception as e:
            print(f"Gagal membuka file: {e}")
            return False

    @staticmethod
    def create_directory(directory_path: str) -> bool:
        """
        Membuat direktori

        Args:
            directory_path (str): Path direktori

        Returns:
            bool: Status pembuatan direktori
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Gagal membuat direktori: {e}")
            return False

    @staticmethod
    def get_file_extension(filename: str) -> Optional[str]:
        """
        Mendapatkan ekstensi file

        Args:
            filename (str): Nama file

        Returns:
            Optional[str]: Ekstensi file
        """
        try:
            return os.path.splitext(filename)[1].lower()
        except Exception:
            return None

    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """
        Mendapatkan ukuran file dalam bytes

        Args:
            file_path (str): Path file

        Returns:
            Optional[int]: Ukuran file dalam bytes
        """
        try:
            return os.path.getsize(file_path)
        except Exception:
            return None

    @staticmethod
    def list_files_in_directory(directory_path: str,
                                extensions: Optional[list] = None) -> list:
        """
        List file dalam direktori dengan filter ekstensi

        Args:
            directory_path (str): Path direktori
            extensions (Optional[list]): Daftar ekstensi yang diizinkan

        Returns:
            list: Daftar file
        """
        try:
            files = os.listdir(directory_path)

            if extensions:
                files = [
                    f for f in files
                    if os.path.splitext(f)[1].lower() in extensions
                ]

            return files
        except Exception as e:
            print(f"Gagal list file: {e}")
            return []

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Membersihkan nama file dari karakter yang tidak valid

        Args:
            filename (str): Nama file

        Returns:
            str: Nama file yang sudah dibersihkan
        """
        # Hapus karakter yang tidak valid
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        cleaned_filename = ''.join(c for c in filename if c in valid_chars)

        # Batasi panjang nama file
        max_length = 255
        return cleaned_filename[:max_length]

    @staticmethod
    def choose_directory() -> Optional[str]:
        """
        Membuka dialog pemilihan direktori

        Returns:
            Optional[str]: Path direktori yang dipilih
        """
        from PySide6.QtWidgets import QFileDialog

        directory = QFileDialog.getExistingDirectory(
            None,
            "Pilih Direktori Download",
            ""
        )
        return directory if directory else None