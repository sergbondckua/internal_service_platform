from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View

from fill_in_docx.services.utils import get_session_key
from fill_in_docx.tasks import generate_documents_task
from fill_in_docx.forms import PartyDataForm
from celery.result import AsyncResult


class ContractGenerateView(FormView):
    """Представлення для генерації документів договору"""

    template_name = "fill_in_docx/generate_contract.html"
    form_class = PartyDataForm
    success_url = reverse_lazy("fill_in_docx:contract_success")

    def form_valid(self, form):
        session_key = get_session_key(self.request)
        result = generate_documents_task.delay(form.cleaned_data, session_key)
        self.request.session["task_id"] = result.id

        return super().form_valid(form)


class ContractSuccessView(TemplateView):
    """Представлення для відображення результату завдання"""

    template_name = "fill_in_docx/contract_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "task_id": self.request.session.get("task_id"),
                "name_organisation": self.request.session.get(
                    "name_organisation", ""
                ),
                "slug_street": self.request.session.get("slug_street", ""),
            }
        )
        return context


class CheckTaskStatusView(View):
    """Представлення для перевірки статусу завдання"""

    def get(self, request, *args, **kwargs):
        task_id = request.GET.get("task_id")
        result = AsyncResult(task_id)
        if result.ready():
            session_key = get_session_key(request)
            dir_session = Path("filled_docx", session_key)
            save_path = settings.MEDIA_ROOT / dir_session
            task_result = result.result or {}

            # Update session data
            request.session.update(
                {
                    "name_organisation": task_result.get(
                        "name_organisation", ""
                    ),
                    "slug_street": task_result.get("slug_street", ""),
                }
            )
            suffix_filled_file = task_result.get("slug_street", "")

            files = {
                "filled_contract_url": f"{settings.MEDIA_URL}{dir_session}/dogovir_{suffix_filled_file}.docx",
                "filled_pax_akt_url": f"{settings.MEDIA_URL}{dir_session}/pax_akt_{suffix_filled_file}.docx",
                "filled_add_agreement_url": f"{settings.MEDIA_URL}{dir_session}/dod_ugoda_{suffix_filled_file}.docx",
            }

            # Check file existence
            available_files = {
                key: url
                for key, url in files.items()
                if (save_path / Path(url).name).exists()
            }
            return JsonResponse(
                {"status": "completed", "files": available_files}
            )

        return JsonResponse({"status": "pending"})
