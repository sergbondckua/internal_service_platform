import locale
import platform

from fill_in_docx.managers.party_data import PartyData
from fill_in_docx.services.declension import NameDeclension
from fill_in_docx.services.numwords import FinancialAmountInUAH

# Встановлюємо українську локаль
locale.setlocale(
    locale.LC_TIME,
    "Ukrainian" if platform.system() == "Windows" else "uk_UA.UTF-8",
)


class DataGenerator:
    """Генерація даних договору"""

    def __init__(self, party_data: PartyData):
        self.party_data = party_data
        self.genitive_name = NameDeclension()
        self.price_in_uah = FinancialAmountInUAH(self.party_data.source_price)
        self.total_price = self.party_data.source_price * 12
        self.total_price_in_uah = FinancialAmountInUAH(self.total_price)

    def generate(self) -> dict:
        """Генерує та повертає дані"""

        person_name_parts = self.party_data.person_name.split()
        short_name = f"{person_name_parts[1]} {person_name_parts[0].upper()}"
        including_electricity_cost = (
            "Вказана вартість включає видатки на сплату спожитої обладнанням Сторони 2 електроенергії."
            if self.party_data.including_electricity_cost
            else ""
        )
        for_osbb_zhbk = (
            " - об’єднання співвласників інфраструктури об’єкта доступу"
            if "СПІВВЛАСНИКІВ" or "КООПЕРАТИВ" in self.party_data.full_name
            else " "
        )
        print(for_osbb_zhbk, flush=True)

        return {
            "contract_number": f"{self.party_data.contract_number}-{self.party_data.date_contract.strftime('%d%m%y')}",
            "old_contract_number": self.party_data.old_contract_number,
            "old_date_contract": (
                self.party_data.old_date_contract.strftime("%d.%m.%Y")
                if self.party_data.old_date_contract
                else ""
            ),
            "city": self.party_data.city,
            "from_date": self.party_data.date_contract.strftime('"%d" %B %Y"'),
            "for_osbb_zhbk": for_osbb_zhbk,
            "party_one": self.party_data.full_name.upper(),
            "party_one_short_name": (
                self.party_data.short_name.upper()
                if self.party_data.short_name
                else self.party_data.full_name.upper()
            ),
            "person_position": self.party_data.person_position,
            "genitive_person_position": self.genitive_name.to_genitive(
                self.party_data.person_position
            ).lower(),
            "person_party_one": self.party_data.person_name,
            "short_name": short_name,
            "genitive_name": self.genitive_name.to_genitive(
                self.party_data.person_name
            ),
            "address": self.party_data.address,
            "price": str(int(self.party_data.source_price)),
            "pennies": f"{self.price_in_uah.extract_pennies():0>2}",
            "price_text": self.price_in_uah.format_result(),
            "total_price_text": self.total_price_in_uah.format_result(),
            "total_price": str(int(self.total_price)),
            "total_pennies": f"{self.total_price_in_uah.extract_pennies():0>2}",
            "including_electricity_cost": including_electricity_cost,
            "person_party_one_phonenumber": self.party_data.phone_number,
            "bank_details": self.party_data.bank_details.strip()
            .replace("\n\n", "\n")
            .replace("\r", ""),
        }
