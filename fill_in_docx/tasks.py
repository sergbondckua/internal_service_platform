from celery import shared_task
from pathlib import Path
from django.conf import settings
from django.core.management import call_command
from slugify import slugify
from fill_in_docx.services.contract_generation_service import generate_contract_documents
from fill_in_docx.services.party_data_service import create_party_data

@shared_task
def generate_documents_task(form_data, session_key):
    """
    Асинхронне завдання для генерації документів.
    """

    # Створюємо унікальний slug для адреси
    slug_street = slugify(
        f"{form_data['street_name'].strip()} {form_data['building_number'].strip()}",
        separator="_",
    )

    # Шлях для збереження файлів, пов'язаних із цим сеансом
    session_folder = Path(settings.MEDIA_ROOT, "filled_docx", session_key)
    session_folder.mkdir(parents=True, exist_ok=True)

    # Створюємо об'єкт PartyData та генеруємо документи
    party_data = create_party_data(form_data)
    generate_contract_documents(party_data, form_data, session_folder)

    # Повертаємо дані для оновлення сеансу
    return {
        "name_organisation": f"{form_data['legal_form']} {form_data['full_name']}".upper(),
        "slug_street": slug_street
    }

@shared_task
def clear_sessions():
    # Виконати команду Django для очищення неактивних сесій
    call_command('clearsessions')