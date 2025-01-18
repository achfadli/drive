import os
import shutil
from typing import List, Optional


class FileManager:
    @staticmethod
    def create_directory(path: str) -> bool:
        """Membuat direktori jika belum ada"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Gagal membuat direktori: {e}")
            return False

    @staticmethod
    def list_files(directory: str, extensions: List[str] = None) -> List[str]:
        """List file dalam direktori dengan filter ekstensi"""
        try:
            files = os.listdir(directory)
            if extensions:
                files = [f for f in files if any(f.endswith(ext) for ext in extensions)]
            return files
        except Exception as e:
            print(f"Gagal list file: {e}")
            return []

    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """Memindahkan file"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Gagal memindahkan file: {e}")
            return False

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Menyalin file"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Gagal menyalin file: {e}")
            return False

    @staticmethod
    def delete_file(path: str) -> bool:
        """Menghapus file"""
        try:
            os.remove(path)
            return True
        except Exception as e:
            print(f"Gagal menghapus file: {e}")
            return False

    @staticmethod
    def get_file_size(path: str) -> Optional[int]:
        """Mendapatkan ukuran file dalam bytes"""
        try:
            return os.path.getsize(path)
        except Exception as e:
            print(f"Gagal mendapatkan ukuran file: {e}")
            return None