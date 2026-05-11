import json
from pathlib import Path


class FileReader:
    """Класс для чтения данных из файлов"""

    def __init__(self, file_path: Path) -> None:
        """Инициализация с путём до файла"""
        self.file_path = file_path

    def read_json(self) -> dict:
        """Чтение данных из JSON файла"""
        with open(self.file_path, encoding="utf-8") as f:
            return json.load(f)
