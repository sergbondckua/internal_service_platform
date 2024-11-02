from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
import os

from fill_in_docx.forms import PartyDataForm
from fill_in_docx.managers.filler import TemplateFiller
from fill_in_docx.managers.party_data import PartyData
from fill_in_docx.managers.generator import DataGenerator
from fill_in_docx.services.utils import clear_directory


class ContractGenerateView(FormView):
    template_name = "fill_in_docx/generate_contract.html"
    form_class = PartyDataForm
    success_url = reverse_lazy("fill_in_docx:contract_success")

    def form_valid(self, form: PartyDataForm):
        # Створення об'єкта PartyData з даних форми

        full_name_organisation = f"{form.cleaned_data['legal_form']} {form.cleaned_data['full_name']}"

        party_data = PartyData(
            contract_number=form.cleaned_data["contract_number"],
            date_contract=form.cleaned_data["date_contract"],
            source_price=form.cleaned_data["source_price"],
            old_contract_number=form.cleaned_data.get(
                "old_contract_number", ""
            ),
            old_date_contract=form.cleaned_data.get("old_date_contract", ""),
            full_name=full_name_organisation,
            short_name=form.cleaned_data.get("short_name", ""),
            address=form.cleaned_data["address"],
            person_position=form.cleaned_data["person_position"],
            person_name=form.cleaned_data["person_name"],
            phone_number=form.cleaned_data["phone_number"],
            city=form.cleaned_data["city"],
            bank_details=form.cleaned_data["bank_details"],
        )

        # Генерація даних для договору
        data_generator = DataGenerator(party_data)
        contract_data = data_generator.generate()

        # Шляхи до шаблонів
        source_dir = os.path.join(settings.BASE_DIR, "fill_in_docx/source/")
        filled_dir = os.path.join(settings.MEDIA_ROOT, "filled_docx")

        # Очищення директорії перед збереженням нових файлів
        clear_directory(filled_dir)

        # Заповнення шаблонів і завантаження результату
        TemplateFiller(
            os.path.join(source_dir, "contract_template.docx"),
            os.path.join(filled_dir, "dogovir.docx"),
        ).fill_template(contract_data)
        TemplateFiller(
            os.path.join(source_dir, "pax_akt_template.docx"),
            os.path.join(filled_dir, "pax_akt.docx"),
        ).fill_template(contract_data)

        # Додаткова угода (якщо є попередній номер договору)
        if contract_data["old_contract_number"]:
            TemplateFiller(
                os.path.join(source_dir, "add_agreement_template.docx"),
                os.path.join(filled_dir, "dod_ugoda.docx"),
            ).fill_template(contract_data)

        return super().form_valid(form)


class ContractSuccessView(TemplateView):
    template_name = "fill_in_docx/contract_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Посилання на файли для завантаження
        context["filled_contract_url"] = os.path.join(
            settings.MEDIA_URL, "filled_docx/dogovir.docx"
        )
        context["filled_pax_akt_url"] = os.path.join(
            settings.MEDIA_URL, "filled_docx/pax_akt.docx"
        )

        # Додаємо додаткову угоду до контексту, якщо вона існує
        add_agreement_path = os.path.join(
            settings.MEDIA_ROOT, "filled_docx/dod_ugoda.docx"
        )
        if os.path.exists(add_agreement_path):
            context["filled_add_agreement_url"] = os.path.join(
                settings.MEDIA_URL, "filled_docx/dod_ugoda.docx"
            )

        return context
