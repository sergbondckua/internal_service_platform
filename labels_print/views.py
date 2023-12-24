from django.shortcuts import render, redirect
from .forms import TagKeyFormSet


class TagKeyView:
    """Create a new tag key."""

    pass


def tag_key_view(request):
    template_name = "labels_print/tag_key.html"
    heading_message = "Formset Demo"
    data = None
    if request.method == "POST":
        formset = TagKeyFormSet(request.POST)
        if formset.is_valid():
            data = [form.cleaned_data for form in formset]
    else:
        formset = TagKeyFormSet()

    context = {"formset": formset, "data": data, "heading": heading_message}
    return render(request, template_name, context)
