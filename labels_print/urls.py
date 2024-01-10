from django.urls import path

from labels_print import views

urlpatterns = [
    path("key/", views.tag_key_view, name="tag_key"),
    path("cell/", views.TagCellFormView.as_view(), name="tag_cell_form"),
]

app_name = "labels_print"
