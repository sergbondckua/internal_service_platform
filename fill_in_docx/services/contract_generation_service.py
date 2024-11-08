import os
from django.conf import settings
from fill_in_docx.managers.filler import TemplateFiller
from fill_in_docx.managers.generator import DataGenerator
from fill_in_docx.services.utils import clear_directory


def determine_text_to_delete(form_data, party_data):
    """Визначає текст, абзац який містить цей текст, потрібно видалити із шаблону."""

    text_to_delete = []
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
    """Генерує документи договору і заповнює шаблони."""
    source_dir = os.path.join(settings.BASE_DIR, "fill_in_docx/source/")
    filled_dir = save_path

    # Очищення директорії перед збереженням нових файлів
    clear_directory(filled_dir)

    # Генерація даних для договору
    contract_data = DataGenerator(party_data).generate()
    text_to_delete = determine_text_to_delete(form_data, party_data)

    templates = [
        ("contract_template.docx", "dogovir.docx"),
        ("pax_akt_template.docx", "pax_akt.docx"),
    ]

    # Заповнення шаблонів
    for source_template, output_file in templates:
        TemplateFiller(
            os.path.join(source_dir, source_template),
            os.path.join(filled_dir, output_file),
        ).fill_and_edit(
            contract_data,
            text_to_delete if "contract" in source_template else [],
        )

    # Додаткова угода (якщо є попередній номер договору)
    if contract_data["old_contract_number"]:
        TemplateFiller(
            os.path.join(source_dir, "add_agreement_template.docx"),
            os.path.join(filled_dir, "dod_ugoda.docx"),
        ).fill_and_edit(contract_data)
