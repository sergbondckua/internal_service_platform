from pathlib import Path

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from slugify import slugify

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
        # Отримуємо очищені дані форми
        form_data = form.cleaned_data

        # Створюємо унікальний slug для адреси (вулиця + номер будинку)
        slug_street = slugify(
            f"{form_data['street_name'].strip()} {form_data['building_number'].strip()}",
            separator="_",
        )

        # Перевіряємо, чи існує ключ сеансу, і створюємо, якщо необхідно
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key

        # Створюємо папку для збереження файлів, пов'язаних із цим сеансом
        session_folder = Path(settings.MEDIA_ROOT, "filled_docx", session_key)
        session_folder.mkdir(parents=True, exist_ok=True)

        # Створюємо об’єкт PartyData та генеруємо документи
        party_data = create_party_data(form_data)
        generate_contract_documents(party_data, form_data, session_folder)

        # Зберігаємо назву організації та адресу у сеансі
        self.request.session["name_organisation"] = (
            f"{form_data['legal_form']} {form_data['full_name']}"
        ).upper()
        self.request.session["slug_street"] = slug_street

        # Викликаємо базову реалізацію form_valid, щоб перенаправити користувача
        return super().form_valid(form)


class ContractSuccessView(TemplateView):
    template_name = "fill_in_docx/contract_success.html"

    def get_context_data(self, **kwargs):
        # Отримуємо початковий контекст
        context = super().get_context_data(**kwargs)

        # Перевіряємо, чи існує ключ сеансу, і створюємо, якщо необхідно
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key

        # Створюємо шляхи до файлів, пов’язаних із сеансом
        dir_session = Path("filled_docx", session_key)
        save_path = Path(settings.MEDIA_ROOT, dir_session)

        # Отримуємо slug для створення назв файлів
        suffix_filled_file = self.request.session.get("slug_street", "")

        # Перевіряємо, чи існує папка з файлами, і додаємо URL файлів у контекст
        if save_path.exists():
            context["filled_contract_url"] = (
                f"{settings.MEDIA_URL}{dir_session}/dogovir_{suffix_filled_file}.docx"
            )
            context["filled_pax_akt_url"] = (
                f"{settings.MEDIA_URL}{dir_session}/pax_akt_{suffix_filled_file}.docx"
            )

            # Додаємо URL додаткової угоди, якщо файл існує
            add_agreement_path = (
                save_path / f"dod_ugoda_{suffix_filled_file}.docx"
            )
            if add_agreement_path.exists():
                context["filled_add_agreement_url"] = (
                    f"{settings.MEDIA_URL}{dir_session}/dod_ugoda_{suffix_filled_file}.docx"
                )

        # Додаємо назву організації у контекст
        context["name_organisation"] = self.request.session.get(
            "name_organisation", ""
        )

        return context
