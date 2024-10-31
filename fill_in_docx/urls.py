from django.urls import path

from fill_in_docx import views

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
]

app_name = "fill_in_docx"
