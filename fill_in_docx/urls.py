from django.urls import path

from fill_in_docx import views
# from fill_in_docx.views import CheckTaskStatusView

urlpatterns = [
    path(
        "contract/",
        views.ContractGenerateView.as_view(),
        name="generate_contract",
    ),
    path(
        "contract_success/",
        views.ContractSuccessView.as_view(),
        name="contract_success",
    ),
    path(
        "check-task-status/",
        views.check_task_status,
        name="check_task_status",
    ),
]

app_name = "fill_in_docx"
