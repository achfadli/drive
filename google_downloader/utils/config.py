import os
import json
from typing import Dict, Any


class ConfigManager:
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Memuat konfigurasi dari file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            return self._create_default_config()
        except Exception:
            return self._create_default_config()

    def _create_default_config(self) -> Dict[str, Any]:
        """Membuat konfigurasi default"""
        default_config = {
            "download_directory": os.path.join(os.path.expanduser("~"), "Downloads", "GoogleDownloader"),
            "max_concurrent_downloads": 3,
            "default_theme": "light",
            "language": "id",
            "auto_open_folder": True,
            "proxy_settings": {
                "use_proxy": False,
                "proxy_url": "",
                "proxy_port": ""
            }
        }
        self.save_config(default_config)
        return default_config

    def get(self, key: str, default: Any = None) -> Any:
        """Mendapatkan nilai konfigurasi"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Mengatur nilai konfigurasi"""
        self.config[key] = value
        self.save_config()

    def save_config(self, config: Dict[str, Any] = None):
        """Menyimpan konfigurasi ke file"""
        try:
            config = config or self.config
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error menyimpan konfigurasi: {e}")