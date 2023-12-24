from django import forms
from django.forms import formset_factory


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
