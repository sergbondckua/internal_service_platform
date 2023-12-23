from django.urls import path

from labels_print import views

urlpatterns = [
    path("", views.tag_key_view, name="tag_key"),
]

app_name = "labels_print"
