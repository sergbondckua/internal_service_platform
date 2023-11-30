from django.db import models
from django.shortcuts import render
from django.views import generic

from search_keys.forms import CellSearchForm
from search_keys.models import Building


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
        prefix = self.request.GET.get("prefix")
        street_name = self.request.GET.get("street_name")
        building_number = self.request.GET.get("building_number")

        if prefix and street_name and building_number:
            cells = self.model.objects.filter(
                models.Q(street__name__contains=street_name)
                | models.Q(street__old_name__contains=street_name),
                models.Q(street__prefix=prefix)
                | models.Q(street__old_prefix=prefix),
                number=building_number,
            )
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
