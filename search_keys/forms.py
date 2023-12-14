from django import forms


class CellSearchForm(forms.Form):
    """Form for searching for cell"""

    street_name = forms.CharField(
        max_length=60,
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Назва вулиці",
                "size": "40",
                "onfocus": "clearInput()",
            }
        ),
    )
    street_id = forms.IntegerField(
        max_value=5,
        label="",
        widget=forms.HiddenInput(),
    )
    building_number = forms.ChoiceField(
        choices=[],
        label="",
        widget=forms.Select(attrs={"required": True}),
    )
