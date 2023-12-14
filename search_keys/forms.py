from django import forms


class CellSearchForm(forms.Form):
    """Form for searching for cell"""

    street_name = forms.CharField(
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
        label="",
        widget=forms.HiddenInput(),
    )
    building_number = forms.ChoiceField(
        choices=[],
        label="",
        widget=forms.Select(attrs={"required": True}),
    )
