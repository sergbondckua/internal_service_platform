import logging
import os
from datetime import datetime
from pathlib import Path

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def clear_directory(directory_path):
    """Видаляє всі файли в зазначеній директорії."""
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) and filename != ".gitkeep":
                os.remove(file_path)
        except Exception as e:
            logging.info(
                f"Помилка видалення %s. Помилка: %s", file_path, str(e)
            )


def get_session_key(request):
    """Генерує або отримує ключ сесії"""
    if not (session_key := request.session.session_key):
        request.session.save()
        session_key = request.session.session_key
    return session_key


def get_available_files(files: dict, save_path: Path) -> dict:
    """
    Перевіряє наявність файлів у заданому каталозі та збирає інформацію про них.
    """
    available_files = {}
    for key, url in files.items():
        # Формуємо повний шлях до файлу на основі save_path та імені файлу з URL
        file_path = save_path / Path(url).name
        # Перевіряємо, чи існує файл за вказаним шляхом
        if file_path.exists():
            available_files[key] = {
                "url": url,
                "name": file_path.name,
                "size": file_path.stat().st_size,  # Розмір файлу в байтах
            }
    return available_files


def get_years():
    """Повертає поточний і попередній рік у форматах yyyy та yy."""
    current_year_full = str(datetime.now().year)
    last_year_full = str(int(current_year_full) - 1)

    # Формати у вигляді двох цифр
    current_year_short = current_year_full[-2:]
    last_year_short = last_year_full[-2:]

    return {
        "current_year_full": current_year_full,
        "last_year_full": last_year_full,
        "current_year_short": current_year_short,
        "last_year_short": last_year_short,
    }
