from django.urls import path

from search_keys import views

urlpatterns = [
    path("", views.CellInfoView.as_view(), name="cell_info"),
    path(
        "street_autocomplete/",
        views.StreetAutocompleteView.as_view(),
        name="street_autocomplete",
    ),
    path(
        "building_autocomplete/",
        views.BuildingAutocompleteView.as_view(),
        name="building_autocomplete",
    ),
    path(
        "api/v1/buildings/",
        views.BuildingListApiView.as_view(),
        name="api_buildings",
    ),
    path(
        "api/v1/cell/",
        views.CellApiView.as_view(),
        name="api_cell",
    ),
    path(
        "api/v1/streets/",
        views.StreetListApiView.as_view(),
        name="api_streets",
    ),
    path(
        "api/v1/street/",
        views.StreetListApiView.as_view(),
        name="api_street",
    ),
]

app_name = "search_keys"
