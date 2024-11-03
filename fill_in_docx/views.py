import os

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from fill_in_docx.forms import PartyDataForm
from fill_in_docx.services.party_data_service import create_party_data
from fill_in_docx.services.contract_generation_service import (
    generate_contract_documents,
)


class ContractGenerateView(FormView):
    template_name = "fill_in_docx/generate_contract.html"
    form_class = PartyDataForm
    success_url = reverse_lazy("fill_in_docx:contract_success")

    def form_valid(self, form):

        # Отримання даних з форми
        form_data = form.cleaned_data

        # Створення об'єкта PartyData з даних форми
        party_data = create_party_data(form_data)

        # Генерація та заповнення шаблонів
        generate_contract_documents(party_data, form_data)

        return super().form_valid(form)


class ContractSuccessView(TemplateView):
    template_name = "fill_in_docx/contract_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filled_contract_url"] = os.path.join(
            settings.MEDIA_URL, "filled_docx/dogovir.docx"
        )
        context["filled_pax_akt_url"] = os.path.join(
            settings.MEDIA_URL, "filled_docx/pax_akt.docx"
        )

        add_agreement_path = os.path.join(
            settings.MEDIA_ROOT, "filled_docx/dod_ugoda.docx"
        )
        if os.path.exists(add_agreement_path):
            context["filled_add_agreement_url"] = os.path.join(
                settings.MEDIA_URL, "filled_docx/dod_ugoda.docx"
            )

        return context
