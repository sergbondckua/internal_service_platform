from django import forms
from django.forms import formset_factory


class TagKeyForm(forms.Form):
    title = forms.CharField(max_length=100)


TagKeyFormSet = formset_factory(TagKeyForm, extra=1)
