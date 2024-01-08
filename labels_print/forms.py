from django import forms
from django.forms import formset_factory

from search_keys.models import Cell


class TagKeyForm(forms.Form):
    title = forms.CharField(
        label="Tag title",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Tag name here",
            }
        ),
    )


TagKeyFormSet = formset_factory(TagKeyForm, extra=1)


class TagCellForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Cell.objects.all().order_by("box", "title"),
        required=True,
        label="",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
                "id": "multiple-select-clear-field",
                "data-placeholder": "Оберіть комірки для друку",
                "multiple": True,
            },
        ),
    )
