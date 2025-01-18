import os
import hashlib
from typing import Optional


class FileSecurityManager:
    @staticmethod
    def generate_file_hash(file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """
        Generate hash file

        Args:
            file_path (str): Path file
            algorithm (str): Algoritma hash (md5, sha1, sha256)

        Returns:
            Optional[str]: Hash file atau None jika gagal
        """
        try:
            hash_algorithm = hashlib.md5() if algorithm == 'md5' else \
                hashlib.sha1() if algorithm == 'sha1' else \
                    hashlib.sha256()

            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_algorithm.update(chunk)

            return hash_algorithm.hexdigest()
        except Exception as e:
            print(f"Gagal generate hash: {e}")
            return None

    @staticmethod
    def is_file_safe(file_path: str) -> bool:
        """
        Cek keamanan file

        Args:
            file_path (str): Path file

        Returns:
            bool: Status keamanan file
        """
        try:
            # Cek ekstensi berbahaya
            dangerous_extensions = ['.exe', '.bat', '.cmd', '.vbs', '.ps1']
            file_ext = os.path.splitext(file_path)[1].lower()

            if file_ext in dangerous_extensions:
                return False

            # Cek ukuran file maksimum
            max_file_size_mb = 500
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

            if file_size_mb > max_file_size_mb:
                return False

            return True
        except Exception as e:
            print(f"Gagal cek keamanan file: {e}")
            return False