from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
import os

from fill_in_docx.forms import PartyDataForm
from fill_in_docx.managers.filler import TemplateFiller
from fill_in_docx.managers.party_data import PartyData
from fill_in_docx.managers.generator import DataGenerator


class ContractGenerateView(FormView):
    template_name = "fill_in_docx/generate_contract.html"
    form_class = PartyDataForm
    success_url = reverse_lazy("fill_in_docx:contract_success")

    def form_valid(self, form: PartyDataForm):
        # Create PartyData object from form data
        party_data = PartyData(
            contract_number=form.cleaned_data["contract_number"],
            date_contract=form.cleaned_data["date_contract"],
            source_price=form.cleaned_data["source_price"],
            old_contract_number=form.cleaned_data.get(
                "old_contract_number", ""
            ),
            old_date_contract=form.cleaned_data.get("old_date_contract", ""),
            full_name=form.cleaned_data["full_name"],
            short_name=form.cleaned_data.get("short_name", ""),
            address=form.cleaned_data["address"],
            person_name=form.cleaned_data["person_name"],
            phone_number=form.cleaned_data["phone_number"],
            city=form.cleaned_data["city"],
            bank_details=form.cleaned_data["bank_details"],
        )

        # Generate contract data
        data_generator = DataGenerator(party_data)
        contract_data = data_generator.generate()

        # Fill templates
        base_dir = "fill_in_docx/source/"
        TemplateFiller(
            os.path.join(base_dir, "contract_template.docx"),
            "media/filled_contract.docx",
        ).fill_template(contract_data)
        TemplateFiller(
            os.path.join(base_dir, "pax_akt_template.docx"),
            "media/filled_pax_akt.docx",
        ).fill_template(contract_data)

        if contract_data["old_contract_number"]:
            TemplateFiller(
                os.path.join(base_dir, "add_agreement_template.docx"),
                "media/filled_add_agreement.docx",
            ).fill_template(contract_data)

        return super().form_valid(form)


class ContractSuccessView(TemplateView):
    template_name = "fill_in_docx/contract_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Посилання на файли для завантаження
        context["filled_contract_url"] = os.path.join(
            settings.MEDIA_URL, "filled_contract.docx"
        )
        context["filled_pax_akt_url"] = os.path.join(
            settings.MEDIA_URL, "filled_pax_akt.docx"
        )
        context["filled_add_agreement_url"] = os.path.join(
            settings.MEDIA_URL, "filled_add_agreement.docx"
        )
        return context
