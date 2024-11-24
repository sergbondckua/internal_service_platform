from django.urls import path

from fill_in_docx import views


urlpatterns = [
    path(
        "",
        views.ContractGenerateView.as_view(),
        name="generate_contract",
    ),
    path(
        "success/",
        views.ContractSuccessView.as_view(),
        name="contract_success",
    ),
    path(
        "check-task-status/",
        views.CheckTaskStatusView.as_view(),
        name="check_task_status",
    ),
]

app_name = "fill_in_docx"
