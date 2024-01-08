from django.urls import path

from labels_print import views

urlpatterns = [
    path("key/", views.tag_key_view, name="tag_key"),
    path("cell/", views.TagCellFormView.as_view(), name="tag_cell_form"),
    path("pdf/<int:pk>/", views.conclusion_to_pdf, name="create_pdf"),
]

app_name = "labels_print"
