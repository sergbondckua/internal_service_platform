import logging
import os


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
