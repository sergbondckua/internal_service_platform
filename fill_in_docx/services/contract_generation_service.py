import os
from django.conf import settings
from slugify import slugify

from fill_in_docx.managers.filler import TemplateFiller
from fill_in_docx.managers.generator import DataGenerator
from fill_in_docx.services.utils import clear_directory


def determine_text_to_delete(form_data, party_data):
    """
    Визначає текст, який потрібно видалити з шаблону на основі даних форми і партії.
    """
    text_to_delete = []

    # Видалення тексту, якщо договір без компенсації за електроенергію
    if (
        not form_data["contract_to_rem"]
        or party_data.including_electricity_cost
    ):
        text_to_delete += [
            "Розрахунки за спожиту електроенергію",
            "Оплата за спожиту",
        ]
    else:
        text_to_delete += ["Оплата за спожиту"]

    # Видалення тексту, якщо розрахунок не за методикою або включено електроенергію
    if (
        party_data.including_electricity_cost
        or not form_data["cost_by_methodic"]
    ):
        text_to_delete += [
            "Розрахунок розміру щомісячної плати",
            "п. 2.8",
            "розміру мінімальної заробітної",
            "спожиту встановленими засобами",
            "Розрахунок розміру щомісячної оплати.",
        ]

    return text_to_delete


def generate_contract_documents(party_data, form_data, save_path):
    """
    Генерує документи договору і заповнює шаблони на основі вхідних даних.

    :param party_data: Об'єкт даних
    :param form_data: Дані форми, введені користувачем
    :param save_path: Шлях, куди зберігати згенеровані документи
    """
    # Шляхи до директорій
    source_dir = os.path.join(settings.BASE_DIR, "fill_in_docx/source/")

    # Очищення директорії перед генерацією нових файлів
    clear_directory(save_path)

    # Генерація даних для заповнення документів
    contract_data = DataGenerator(party_data).generate()
    text_to_delete = determine_text_to_delete(form_data, party_data)

    # Формування суфіксу для імен файлів на основі адреси
    suffix_filled_file = slugify(
        f"{form_data['street_name'].strip()} {form_data['building_number'].strip()}",
        separator="_",
    )

    # Шаблони документів і їх результуючі імена
    templates = [
        ("contract_template.docx", f"dogovir_{suffix_filled_file}.docx"),
        ("pax_akt_template.docx", f"pax_akt_{suffix_filled_file}.docx"),
    ]

    # Заповнення шаблонів
    for source_template, output_file in templates:
        TemplateFiller(
            os.path.join(source_dir, source_template),
            os.path.join(save_path, output_file),
        ).fill_and_edit(
            contract_data,
            text_to_delete if "contract" in source_template else [],
        )

    # Генерація додаткової угоди, якщо вказаний попередній номер договору
    if contract_data.get("old_contract_number"):
        TemplateFiller(
            os.path.join(source_dir, "add_agreement_template.docx"),
            os.path.join(save_path, f"dod_ugoda_{suffix_filled_file}.docx"),
        ).fill_and_edit(contract_data)
