import re
from urllib.parse import urlparse
from typing import Dict, Any


class URLValidator:
    SUPPORTED_PLATFORMS = [
        'drive.google.com',
        'docs.google.com',
        'docs.google.com/document',
        'docs.google.com/presentation',
        'docs.google.com/spreadsheets'
    ]

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validasi URL umum

        Args:
            url (str): URL yang akan divalidasi

        Returns:
            bool: True jika URL valid, False sebaliknya
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_google_drive_url(url: str) -> bool:
        """
        Validasi URL Google Drive

        Args:
            url (str): URL Google Drive

        Returns:
            bool: True jika URL Google Drive valid, False sebaliknya
        """
        try:
            parsed_url = urlparse(url)
            return (
                    parsed_url.netloc == 'drive.google.com' and
                    '/file/d/' in parsed_url.path
            )
        except Exception:
            return False

    @staticmethod
    def validate_google_docs_url(url: str) -> bool:
        """
        Validasi URL Google Docs, Slides, Sheets

        Args:
            url (str): URL Google Docs

        Returns:
            bool: True jika URL Google Docs valid, False sebaliknya
        """
        try:
            parsed_url = urlparse(url)
            return (
                    parsed_url.netloc == 'docs.google.com' and
                    any(doc_type in parsed_url.path for doc_type in [
                        '/document',
                        '/presentation',
                        '/spreadsheets'
                    ])
            )
        except Exception:
            return False

    @staticmethod
    def extract_file_id(url: str) -> str:
        """
        Ekstrak file ID dari URL Google

        Args:
            url (str): URL Google Drive/Docs

        Returns:
            str: File ID atau string kosong
        """
        try:
            if 'drive.google.com' in url:
                # Google Drive
                match = re.search(r'/file/d/([^/]+)', url)
            elif 'docs.google.com' in url:
                # Google Docs/Slides/Sheets
                match = re.search(r'/d/([^/]+)', url)
            else:
                return ""

            return match.group(1) if match else ""
        except Exception:
            return ""

    @staticmethod
    def get_url_info(url: str) -> Dict[str, Any]:
        """
        Mendapatkan informasi detail URL

        Args:
            url (str): URL untuk dianalisis

        Returns:
            Dict berisi informasi URL
        """
        try:
            parsed_url = urlparse(url)
            return {
                'valid': URLValidator.validate_url(url),
                'scheme': parsed_url.scheme,
                'netloc': parsed_url.netloc,
                'path': parsed_url.path,
                'is_google_drive': URLValidator.validate_google_drive_url(url),
                'is_google_docs': URLValidator.validate_google_docs_url(url),
                'file_id': URLValidator.extract_file_id(url)
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

    @classmethod
    def is_supported_platform(cls, url: str) -> bool:
        """
        Cek apakah platform URL didukung

        Args:
            url (str): URL untuk dicek

        Returns:
            bool: True jika platform didukung, False sebaliknya
        """
        parsed_url = urlparse(url)
        return any(platform in parsed_url.netloc for platform in cls.SUPPORTED_PLATFORMS)