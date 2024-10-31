import locale
import platform

from fill_in_docx.managers.party_data import PartyData
from fill_in_docx.services.declension import NameDeclension
from fill_in_docx.services.numwords import FinancialAmountInUAH


# Встановлюємо українську локаль
if platform.system() == "Windows":
    locale.setlocale(locale.LC_TIME, "Ukrainian")
else:
    locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")


class DataGenerator:
    """Генерація даних договору"""

    def __init__(self, party_data: PartyData):
        self.party_data = party_data
        self.genitive_name = NameDeclension()

    def generate(self) -> dict:
        """Генерує та повертає дані"""

        price_text = FinancialAmountInUAH(
            self.party_data.source_price
        ).format_result()
        total_price = self.party_data.source_price * 12
        total_price_text = FinancialAmountInUAH(total_price).format_result()

        part_person_name = self.party_data.person_name.split()
        short_name = f"{part_person_name[1]} {part_person_name[0].upper()}"

        return {
            "contract_number": f"{self.party_data.contract_number}"
                               f"-{self.party_data.date_contract.strftime('%d%m%y')}",
            "old_contract_number": self.party_data.old_contract_number,
            "old_date_contract": self.party_data.old_date_contract.strftime(
                "%d.%m.%Y"
            ),
            "city": self.party_data.city,
            "from_date": self.party_data.date_contract.strftime("%d %B %Y"),
            "party_one": self.party_data.full_name.upper(),
            "party_one_short_name": (
                self.party_data.short_name.upper()
                if self.party_data.short_name
                else self.party_data.full_name.upper()
            ),
            "person_party_one": self.party_data.person_name,
            "short_name": short_name,
            "genitive_name": self.genitive_name.to_genitive(
                self.party_data.person_name
            ),
            "address": self.party_data.address,
            "price": str(int(self.party_data.source_price)),
            "pennies": f"{FinancialAmountInUAH(self.party_data.source_price).extract_pennies()}0"[
                :2
            ],
            "price_text": price_text,
            "total_price_text": total_price_text,
            "total_price": f"{int(total_price)}",
            "total_pennies": f"{FinancialAmountInUAH(total_price).extract_pennies()}0"[
                :2
            ],
            "person_party_one_phonenumber": self.party_data.phone_number,
            "bank_details": self.party_data.bank_details.strip()
            .replace("\n\n", "\n")
            .replace("\r", ""),
        }
