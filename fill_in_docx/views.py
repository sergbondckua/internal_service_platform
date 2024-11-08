import os
from pathlib import Path

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

        # Переконуємось, що сесія має ключ
        if not self.request.session.session_key:
            self.request.session.save()  # Зберігає сесію, створюючи session_key, якщо він відсутній

        # Створення шляху до каталогу для збереження файлів
        session_folder = (
            Path(settings.MEDIA_ROOT)
            / "filled_docx"
            / self.request.session.session_key
        )
        session_folder.mkdir(parents=True, exist_ok=True)

        # Створення об'єкта PartyData з даних форми
        party_data = create_party_data(form_data)

        # Генерація та заповнення шаблонів
        generate_contract_documents(party_data, form_data, session_folder)

        # Збереження назви компанії в сесії
        self.request.session["name_organisation"] = (
            # f"{form_data['legal_form']} {form_data['full_name']}"
            self.request.session.session_key
        )

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

        # Отримання даних з сесії
        context["name_organisation"] = self.request.session.get(
            "name_organisation"
        )

        return context
