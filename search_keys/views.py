from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic, View

from rest_framework.response import Response
from rest_framework.views import APIView

from search_keys.serializers import (
    BuildingListSerializer,
    StreetListSerializer,
    CellListSerializer,
)
from search_keys.forms import CellSearchForm
from search_keys.models import Building, Street, Cell, Box


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


class BoxListApiView(APIView):
    """View for retrieving a list of boxes."""

    def get(self, request):
        boxes = Box.objects.all().order_by("title")
        serializer = StreetListSerializer(boxes, many=True)
        return Response(serializer.data)


class CellListApiView(APIView):
    """View for retrieving a list of cells."""

    def get(self, request):
        cells = Cell.objects.all().order_by("title")
        serializer = CellListSerializer(cells, many=True)
        return Response(serializer.data)


class StreetListApiView(APIView):
    """View for retrieving a list of streets."""

    def get(self, request):
        streets = Street.objects.all().order_by("id")
        serializer = StreetListSerializer(streets, many=True)
        return Response(serializer.data)


class BuildingListApiView(APIView):
    """View for retrieving a list of addresses buildings."""

    def get(self, request):
        building = Building.objects.all().order_by("id")
        serializer = BuildingListSerializer(building, many=True)
        return Response(serializer.data)


class CellDetailApiView(APIView):
    """Retrieving Cell objects based on street and building number."""

    def get(self, request):
        street_id = request.GET.get("street")
        number = request.GET.get("number")

        # Validate parameters
        if not street_id or not number:
            error_response = {
                "error": "Both 'street' and 'number' parameters are required."
            }
            return Response(error_response, status=400)

        try:
            # Retrieve cells based on street and number
            cell = Cell.objects.get(
                building__street_id=street_id, building__number=number
            )
            serializer = CellListSerializer(cell)
            return Response(serializer.data)
        except Cell.DoesNotExist:
            error_response = {
                "error": "No cells found for the specified parameters."
            }
            return Response(error_response, status=404)


class StreetDetailApiView(APIView):
    """Retrieves information about a specific street"""

    def get(self, request):
        street_name = request.GET.get("name")
        prefix = request.GET.get("prefix")

        # Validate parameters
        if not street_name or not prefix:
            error_response = {
                "error": "Both 'name' and 'prefix' parameters are required."
            }
            return Response(error_response, status=400)

        try:
            # Retrieve cells based on street and number
            street = Street.objects.get(
                Q(name__icontains=street_name)
                | Q(old_name__icontains=street_name),
                Q(prefix=prefix) | Q(old_prefix=prefix),
            )
            serializer = StreetListSerializer(street)
            return Response(serializer.data)
        except Street.DoesNotExist:
            error_response = {
                "error": "No street found for the specified parameters."
            }
            return Response(error_response, status=404)
