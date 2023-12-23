from django.shortcuts import render, redirect
from .forms import TagKeyFormSet


class TagKeyView:
    """Create a new tag key."""

    pass


def tag_key_view(request):
    data = None
    if request.method == "POST":
        formset = TagKeyFormSet(request.POST)
        if formset.is_valid():
            data = [form.cleaned_data for form in formset]
    else:
        formset = TagKeyFormSet()

    context = {"formset": formset, "data": data}
    return render(request, "labels_print/tag_key.html", context)
