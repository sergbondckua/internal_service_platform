from rest_framework import serializers
from search_keys.models import Building, Street, Cell, Box


class BoxListSerializer(serializers.ModelSerializer):
    """Serializer for Box"""

    class Meta:
        model = Box
        exclude = ("created_at", "updated_at")


class CellSerializer(serializers.ModelSerializer):
    """Serializer for Cell"""

    box = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Cell
        exclude = ("created_at", "updated_at")


class StreetListSerializer(serializers.ModelSerializer):
    """Serializer for Street"""

    class Meta:
        model = Street
        exclude = ("created_at", "updated_at")


class BuildingListSerializer(serializers.ModelSerializer):
    """Serializer for Building"""

    cell = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Building
        exclude = ("created_at", "updated_at")
