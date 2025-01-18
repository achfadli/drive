import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    def __init__(self, log_dir: str = 'logs'):
        # Buat direktori log jika belum ada
        os.makedirs(log_dir, exist_ok=True)

        # Generate nama file log unik
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"download_log_{timestamp}.log")

        # Konfigurasi logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str):
        """Log informasi"""
        self.logger.info(message)
        print(f"ℹ️ {message}")

    def log_error(self, message: str, error: Optional[Exception] = None):
        """Log error"""
        if error:
            self.logger.error(f"{message}: {str(error)}")
            print(f"❌ {message}: {str(error)}")
        else:
            self.logger.error(message)
            print(f"❌ {message}")

    def log_warning(self, message: str):
        """Log peringatan"""
        self.logger.warning(message)
        print(f"⚠️ {message}")

    def log_success(self, message: str):
        """Log keberhasilan"""
        self.logger.info(message)
        print(f"✅ {message}")