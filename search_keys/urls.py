from django.urls import path

from search_keys import views
from search_keys.views import CellInfoView, StreetAutocompleteView

urlpatterns = [
    path("", views.BuildingsListView.as_view(), name="index"),
    path("cell_info/", CellInfoView.as_view(), name="cell_info"),
    path(
        "street_autocomplete/",
        StreetAutocompleteView.as_view(),
        name="street_autocomplete",
    ),
]

app_name = "search_keys"
