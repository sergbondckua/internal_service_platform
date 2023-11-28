from django.db import models
from django.shortcuts import get_object_or_404
from django.views import generic

from search_keys.models import Building, Street


class BuildingsListView(generic.ListView):
    """TODO: Remove"""

    model = Building
    template_name = "search_key/building_list.html"


class CellInfoView(generic.TemplateView):
    """
    View for displaying cell information based on street and building number.
    """

    template_name = "search_key/cell_info.html"

    def get_context_data(self, **kwargs):
        """
        Override the base class method to provide additional context data.
        """
        context = super().get_context_data(**kwargs)
        prefix = self.request.GET.get("prefix", "")
        street_name = self.request.GET.get("street_name", "")
        building_number = self.request.GET.get("building_number", "")

        cell_title = self.get_cell_title(prefix, street_name, building_number)
        context["cell_title"] = cell_title
        return context

    @staticmethod
    def get_cell_title(prefix, street_name, building_number):
        """
        Get the cell title based on the given street name and building number.
        """
        street = get_object_or_404(
            Street,
            models.Q(name=street_name) | models.Q(old_name=street_name),
            models.Q(prefix=prefix) | models.Q(old_prefix=prefix),
        )

        building = get_object_or_404(
            Building, street=street, number=building_number
        )
        return building.cell.title
