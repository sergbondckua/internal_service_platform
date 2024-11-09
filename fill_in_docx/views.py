from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from fill_in_docx.tasks import generate_documents_task
from fill_in_docx.forms import PartyDataForm
from celery.result import AsyncResult

def get_session_key(request):
    """Генерує або отримує ключ сесії"""
    if not (session_key := request.session.session_key):
        request.session.save()
        session_key = request.session.session_key
    return session_key

class ContractGenerateView(FormView):
    template_name = "fill_in_docx/generate_contract.html"
    form_class = PartyDataForm
    success_url = reverse_lazy("fill_in_docx:contract_success")

    def form_valid(self, form):
        session_key = get_session_key(self.request)
        result = generate_documents_task.delay(form.cleaned_data, session_key)
        self.request.session["task_id"] = result.id

        return super().form_valid(form)

class ContractSuccessView(TemplateView):
    template_name = "fill_in_docx/contract_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "task_id": self.request.session.get("task_id"),
            "name_organisation": self.request.session.get("name_organisation", ""),
            "slug_street": self.request.session.get("slug_street", ""),
        })
        return context

def check_task_status(request):
    task_id = request.GET.get("task_id")
    result = AsyncResult(task_id)
    if result.ready():
        session_key = get_session_key(request)
        dir_session = Path("filled_docx", session_key)
        save_path = settings.MEDIA_ROOT / dir_session
        task_result = result.result or {}

        # Оновлюємо дані сесії
        request.session.update({
            "name_organisation": task_result.get("name_organisation", ""),
            "slug_street": task_result.get("slug_street", "")
        })
        suffix_filled_file = task_result.get("slug_street", "")

        files = {
            "filled_contract_url": f"{settings.MEDIA_URL}{dir_session}/dogovir_{suffix_filled_file}.docx",
            "filled_pax_akt_url": f"{settings.MEDIA_URL}{dir_session}/pax_akt_{suffix_filled_file}.docx",
            "filled_add_agreement_url": f"{settings.MEDIA_URL}{dir_session}/dod_ugoda_{suffix_filled_file}.docx",
        }

        # Перевіряємо існування файлів
        available_files = {
            key: url for key, url in files.items() if (save_path / Path(url).name).exists()
        }
        return JsonResponse({"status": "completed", "files": available_files})
    return JsonResponse({"status": "pending"})
