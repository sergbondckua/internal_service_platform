from django.urls import path

from search_keys import views
from search_keys.views import CellInfoView

urlpatterns = [
    path("", views.BuildingsListView.as_view(), name="index"),
    path("cell_info/", CellInfoView.as_view(), name="cell_info"),
]

app_name = "search_keys"
