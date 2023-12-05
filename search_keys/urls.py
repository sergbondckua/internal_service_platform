from django.urls import path

from search_keys.views import (
    CellInfoView,
    StreetAutocompleteView,
    BuildingAutocompleteView,
)

urlpatterns = [
    path("", CellInfoView.as_view(), name="cell_info"),
    path(
        "street_autocomplete/",
        StreetAutocompleteView.as_view(),
        name="street_autocomplete",
    ),
    path(
        "building_autocomplete/",
        BuildingAutocompleteView.as_view(),
        name="building_autocomplete",
    ),
]

app_name = "search_keys"
