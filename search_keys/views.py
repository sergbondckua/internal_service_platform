from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic, View

from search_keys.forms import CellSearchForm
from search_keys.models import Building, Street


class BuildingsListView(generic.ListView):
    """TODO: Remove"""

    model = Building
    template_name = "search_key/building_list.html"


class CellInfoView(generic.TemplateView):
    """
    View for displaying cell information based on street and building number.
    """

    model = Building
    template_name = "search_key/cell_info.html"
    context_object_name = "cells"

    def get_queryset(self):
        street_id = self.request.GET.get("street_id")
        building_number = self.request.GET.get("building_number")

        if street_id and building_number:
            cells = self.model.objects.filter(
                street=street_id, number=building_number)
            return cells

        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CellSearchForm(self.request.GET or None)
        return context

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        form = CellSearchForm()

        if queryset is not None:
            return render(
                request,
                self.template_name,
                {"cells": queryset, "form": self.get_context_data()["form"]},
            )
        return render(request, self.template_name, {"form": form})


class StreetAutocompleteView(View):
    """Autocomplete view for street"""

    model = Street

    def get(self, request):
        term = request.GET.get("term", "")
        print(term)
        streets = self.model.objects.filter(
            Q(name__contains=term) | Q(old_name__contains=term)
        )[:10]
        result = [
            {"named": str(street), "street_id": street.id} for street in streets
        ]
        return JsonResponse(result, safe=False)
