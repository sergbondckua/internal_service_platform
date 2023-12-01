from django.contrib import admin

from common.admin import BaseAdmin
from search_keys.models import Box, Building, Cell, Street


class BuildingInline(admin.TabularInline):
    model = Building
    extra = 1


@admin.register(Box)
class BoxAdmin(BaseAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)
    save_on_top = True

    fieldsets = (
        (
            "Identifier box",
            {
                "fields": (
                    "id",
                    "title",
                )
            },
        ),
    ) + BaseAdmin.fieldsets


@admin.register(Cell)
class CellAdmin(BaseAdmin):
    inlines = [BuildingInline]
    list_display = (
        "title",
        "box",
    )
    list_filter = (
        "title",
        "box",
    )
    search_fields = (
        "title",
        "box",
    )
    save_on_top = True

    fieldsets = (
        (
            "Identifier cell",
            {
                "fields": (
                    "id",
                    "title",
                    "box",
                )
            },
        ),
    ) + BaseAdmin.fieldsets


@admin.register(Street)
class StreetAdmin(BaseAdmin):
    list_display = (
        "prefix",
        "name",
        "old_prefix",
        "old_name",
    )
    list_display_links = (
        "name",
        "old_name",
    )
    list_filter = (
        "prefix",
        "name",
        "old_prefix",
        "old_name",
    )
    search_fields = (
        "name",
        "old_name",
    )
    save_on_top = True
    fieldsets = (
        (
            "Identifier Street",
            {
                "fields": (
                    "id",
                    "prefix",
                    "name",
                    "old_prefix",
                    "old_name",
                )
            },
        ),
    ) + BaseAdmin.fieldsets


@admin.register(Building)
class BuildingAdmin(BaseAdmin):
    list_display = (
        "cell",
        "street",
        "number",
    )
    list_filter = (
        "cell",
        "street",
        "number",
    )
    search_fields = (
        "cell",
        "street",
        "number",
    )
    save_on_top = True
    save_as = True
    fieldsets = (
        (
            "Identifier building number",
            {
                "fields": (
                    "id",
                    "cell",
                    "street",
                    "number",
                )
            },
        ),
    ) + BaseAdmin.fieldsets
