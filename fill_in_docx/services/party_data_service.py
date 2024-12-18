from fill_in_docx.enums import LegalFormChoices
from fill_in_docx.managers.party_data import PartyData


def create_party_data(form_data):
    """
    Створює об'єкт PartyData з даних форми.

    :param form_data: Дані, отримані з форми.
    :return: Ініціалізований об'єкт PartyData.
    """
    # Формування повної назви організації
    name = form_data["full_name"].strip(' "')
    full_name_organisation = f'{form_data["legal_form"]} "{name}"'

    # Формування короткої назви організації
    if form_data.get("is_short_name"):
        legal_form_label = next(
            (
                choice[1]
                for choice in LegalFormChoices.choices
                if choice[0] == form_data.get("legal_form")
            )
        )
        short_name_organisation = (
            f'{legal_form_label} "{name}"'
            if legal_form_label
            else full_name_organisation
        )
    else:
        short_name_organisation = full_name_organisation

    # Формування адреси
    address = (
        f"{form_data['city_obj_type']} {form_data['street_name'].strip().title()}, "
        f"будинок {form_data['building_number'].strip()}"
    )

    # Генерація номера договору з урахуванням суфікса, якщо він потрібен
    contract_number = (
        f"{form_data['contract_number'].strip()}-{form_data['date_contract'].strftime('%d%m%y')}"
        if form_data["is_suffix_number"]
        else form_data["contract_number"].strip()
    )

    # Створення та повернення об'єкта PartyData
    return PartyData(
        contract_number=contract_number,
        date_contract=form_data["date_contract"],  # Дата укладання договору
        source_price=form_data["source_price"],  # Базова вартість
        including_electricity_cost=form_data[
            "including_electricity_cost"
        ],  # Враховує вартість електроенергії
        old_contract_number=form_data.get(
            "old_contract_number", ""
        ),  # Попередній номер договору (якщо є)
        old_date_contract=form_data.get(
            "old_date_contract", ""
        ),  # Дата попереднього договору
        full_name=full_name_organisation,  # Повна назва організації
        short_name=short_name_organisation,  # Скорочена назва (опційно)
        address=address,  # Адреса організації
        person_position=form_data[
            "person_position"
        ],  # Посада відповідальної особи
        person_name=form_data[
            "person_name"
        ].strip(),  # Ім'я відповідальної особи
        phone_number=form_data["phone_number"].strip(),  # Номер телефону
        city=form_data["city"].strip(),  # Місто
        bank_details=form_data["bank_details"],  # Банківські реквізити
    )
