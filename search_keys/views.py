from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic, View

from search_keys.forms import CellSearchForm
from search_keys.models import Building, Street


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
                street=street_id, number=building_number
            )
            return cells

        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        street_id = self.request.GET.get("street_id", "")
        building_choices = [
            (building.number, str(building.number))
            for building in self.model.objects.filter(street=street_id)
        ]
        form = CellSearchForm(self.request.GET or None)
        form.fields["building_number"].choices = building_choices
        context["form"] = form
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
        streets = self.model.objects.filter(
            Q(name__icontains=term) | Q(old_name__icontains=term)
        )[:10]
        result = [
            {"named": str(street), "street_id": street.id}
            for street in streets
        ]
        return JsonResponse(result, safe=False)


class BuildingAutocompleteView(View):
    """Autocomplete view for building"""

    model = Building

    def get(self, request):
        term = request.GET.get("term", "")
        street_id = request.GET.get("street_id", "")

        buildings = (
            self.model.objects.filter(
                Q(street=street_id) & Q(number__icontains=term)
            )
            .values("number")
            .distinct()
        )

        building_list = [
            {"building_number": building["number"]} for building in buildings
        ]

        return JsonResponse(building_list, safe=False)
