from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from labels_print.common.pdfmaker import PDFGenerator
from labels_print.forms import TagKeyFormSet, TagCellForm


class TagKeyView:
    """Create a new tag key."""


def tag_key_view(request):
    template_name = "labels_print/tag_key.html"
    data = None
    if request.method == "POST":
        formset = TagKeyFormSet(request.POST)
        if formset.is_valid():
            data = [form.cleaned_data for form in formset]
    else:
        formset = TagKeyFormSet()

    context = {"formset": formset, "data": data}
    return render(request, template_name, context)


class TagCellFormView(generic.FormView, generic.TemplateView):
    template_name = "labels_print/tag_cell_print.html"
    form_class = TagCellForm

    def form_valid(self, form):
        selected_cells = form.cleaned_data["tags"]
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "filename=label_print.pdf"
        pdf_generator = PDFGenerator(response, selected_cells)
        pdf_generator.generate_pdf_doc()
        return response
