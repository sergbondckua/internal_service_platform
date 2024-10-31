from datetime import datetime

from django import forms


class PartyDataForm(forms.Form):
    contract_number = forms.CharField(
        label="Номер договору",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "15",
                "placeholder": "ОСББ-001-01012024",
            }
        ),
    )
    date_contract = forms.DateField(
        label="Дата договору",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "value": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
                "type": "date",
            }
        ),
    )
    source_price = forms.FloatField(
        label="Ціна за місяць",
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "step": "0.01",
                "min": "1.00",
                "placeholder": "1.00",
                "class": "form-control",
                "size": "6",
            }
        ),
    )
    old_contract_number = forms.CharField(
        label="Попередній номер договору",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "20",
                "placeholder": "Якщо є, для дод. уг. на припинення дії цього договору",
            }
        ),
    )
    old_date_contract = forms.DateField(
        label="Дата старого договору",
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    full_name = forms.CharField(
        label="Повне найменування юр. особи",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "50",
                "placeholder": 'ОБ\'ЄДНАННЯ СПІВВЛАСНИКІВ БАГАТОКВАРТИРНОГО БУДИНКУ "БАРВІНОК"',
            }
        ),
    )
    short_name = forms.CharField(
        label="Скорочена назва",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "30",
                "placeholder": 'ОСББ "БАРВІНОК"',
            }
        ),
    )
    address = forms.CharField(
        label="Місцезнаходження юридичної особи",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "50",
                "placeholder": "м. Місто, вулиця Вулиця, будинок 000",
            }
        ),
    )
    person_name = forms.CharField(
        label="Уповноважена особа",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "30",
                "placeholder": "Прізвище Ім'я По батькові",
            }
        ),
    )
    phone_number = forms.CharField(
        label="Номер телефону уповноваженоїособи",
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "15",
                "placeholder": "097-123-45-67",
            }
        ),
    )
    city = forms.CharField(
        label="Місто",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "size": "30",
                "value": "Черкаси",
            }
        ),
    )
    bank_details = forms.CharField(
        label="Банківські реквізити",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": "7",
                "cols": "30",
                "placeholder": """00000, м. Місто, вул. Вулиця, 000
р/р UA000000000000000000000000000
в АТ КБ "Банк"
МФО 654321
ЄДРПОУ 12345678
т. 097-123-45-67"""
            }
        ),
        required=True,
    )
