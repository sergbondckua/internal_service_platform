from django import forms

from search_keys.enums import PrefixStreetChoices


class CellSearchForm(forms.Form):
    """Form for searching for cell"""

    prefix = forms.ChoiceField(
        label="",
        choices=PrefixStreetChoices.choices,
        widget=forms.Select(),
        initial=PrefixStreetChoices.ST
    )
    street_name = forms.CharField(
        max_length=50,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Назва вулиці"}),
    )
    building_number = forms.CharField(
        max_length=10,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "№ будинку", "size": "10"})
    )
