from django.urls import path

from labels_print import views

urlpatterns = [
    path("", views.tag_key_view, name="tag_key"),
    path("pdf/<int:pk>/", views.conclusion_to_pdf, name="create_pdf"),
]

app_name = "labels_print"
