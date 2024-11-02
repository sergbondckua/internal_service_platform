from dataclasses import dataclass
from datetime import datetime


@dataclass
class PartyData:
    """Дані для створення договору"""

    contract_number: str
    date_contract: datetime
    source_price: float
    old_contract_number: str
    old_date_contract: datetime | str
    full_name: str
    short_name: str
    address: str
    person_position: str
    person_name: str
    phone_number: str
    city: str
    bank_details: str
