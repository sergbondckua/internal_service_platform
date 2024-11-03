from fill_in_docx.managers.party_data import PartyData


def create_party_data(form_data):
    """Створює об'єкт PartyData з даних форми."""
    full_name_organisation = (
        f"{form_data['legal_form']} {form_data['full_name']}"
    )
    address = f"{form_data['city_obj_type']} {form_data['street_name']}, будинок {form_data['building_number']}"

    return PartyData(
        contract_number=form_data["contract_number"],
        date_contract=form_data["date_contract"],
        source_price=form_data["source_price"],
        including_electricity_cost=form_data["including_electricity_cost"],
        old_contract_number=form_data.get("old_contract_number", ""),
        old_date_contract=form_data.get("old_date_contract", ""),
        full_name=full_name_organisation,
        short_name=form_data.get("short_name", ""),
        address=address,
        person_position=form_data["person_position"],
        person_name=form_data["person_name"],
        phone_number=form_data["phone_number"],
        city=form_data["city"],
        bank_details=form_data["bank_details"],
    )
