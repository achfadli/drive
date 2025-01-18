import os
import requests
import gdown
import threading
from typing import Optional, Union
from urllib.parse import urlparse


class Downloader:
    def __init__(self, output_dir: str = './downloads'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def validate_url(self, url: str) -> bool:
        """Validasi URL yang didukung"""
        supported_domains = [
            'drive.google.com',
            'docs.google.com',
            'docs.google.com/document',
            'docs.google.com/presentation',
            'docs.google.com/spreadsheets'
        ]
        parsed_url = urlparse(url)
        return any(domain in parsed_url.netloc for domain in supported_domains)

    def get_file_name(self, url: str, response=None) -> str:
        """Mendapatkan nama file dari URL atau header"""
        if response and 'Content-Disposition' in response.headers:
            # Coba ambil nama file dari header
            filename = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
        else:
            # Gunakan bagian terakhir dari URL
            filename = os.path.basename(urlparse(url).path)

        # Jika nama file kosong, gunakan ID atau timestamp
        if not filename:
            filename = f"download_{int(time.time())}"

        return filename

    def download_google_drive(self, url: str) -> Optional[str]:
        """Download file dari Google Drive"""
        try:
            # Ekstrak file ID
            file_id = url.split('/')[-2]
            prefix = 'https://drive.google.com/uc?export=download&id='
            full_url = prefix + file_id

            # Generate nama file
            filename = f"{file_id}_gdrive_download"
            output_path = os.path.join(self.output_dir, filename)

            # Download menggunakan gdown
            gdown.download(full_url, output=output_path, quiet=False)

            return output_path
        except Exception as e:
            print(f"Gagal download Google Drive: {e}")
            return None

    def download_google_docs(self, url: str) -> Optional[str]:
        """Download dokumen atau presentasi Google"""
        try:
            if 'document/d/' in url:
                # Google Docs
                file_id = url.split('/d/')[1].split('/')[0]
                download_url = f'https://docs.google.com/document/d/{file_id}/export?format=docx'
                filename = f"{file_id}.docx"
            elif 'presentation/d/' in url:
                # Google Slides
                file_id = url.split('/d/')[1].split('/')[0]
                download_url = f'https://docs.google.com/presentation/d/{file_id}/export/pptx'
                filename = f"{file_id}.pptx"
            elif 'spreadsheets/d/' in url:
                # Google Sheets
                file_id = url.split('/d/')[1].split('/')[0]
                download_url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx'
                filename = f"{file_id}.xlsx"
            else:
                raise ValueError("URL Google Docs tidak valid")

            # Download file
            response = requests.get(download_url)

            if response.status_code == 200:
                output_path = os.path.join(self.output_dir, filename)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return output_path
            else:
                print(f"Gagal download: Status code {response.status_code}")
                return None

        except Exception as e:
            print(f"Gagal download Google Docs: {e}")
            return None

    def download_direct_link(self, url: str) -> Optional[str]:
        """Download dari direct link"""
        try:
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                filename = self.get_file_name(url, response)
                output_path = os.path.join(self.output_dir, filename)

                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                return output_path
            else:
                print(f"Gagal download: Status code {response.status_code}")
                return None

        except Exception as e:
            print(f"Gagal download direct link: {e}")
            return None

    def download(self, url: str) -> Optional[str]:
        """Metode utama download dengan deteksi otomatis"""
        if not self.validate_url(url):
            print("URL tidak didukung")
            return None

        if 'drive.google.com' in url:
            return self.download_google_drive(url)
        elif 'docs.google.com' in url:
            return self.download_google_docs(url)
        else:
            return self.download_direct_link(url)