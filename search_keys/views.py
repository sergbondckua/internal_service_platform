from django.db import models
from django.shortcuts import get_object_or_404, render
from django.views import generic

from search_keys.forms import CellSearchForm
from search_keys.models import Building, Street, Cell


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
        context = super().get_context_data(**kwargs)
        context["form"] = CellSearchForm(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        form = CellSearchForm(request.GET)
        if form.is_valid():
            prefix = form.cleaned_data.get("prefix")
            street_name = form.cleaned_data.get("street_name")
            building_number = form.cleaned_data.get("building_number")

            # Формируем параметры для фильтрации
            filters = {}
            if prefix:
                filters["street__prefix"] = prefix
            if street_name:
                filters["street__name__iexact"] = street_name
            if building_number:
                filters["number"] = building_number

            # Выполняем поиск в базе данных
            cells = Building.objects.filter(**filters)

            return render(
                request,
                "search_key/results.html",
                {"cells": cells, "form": form},
            )

        return render(request, self.template_name, {"form": form})
