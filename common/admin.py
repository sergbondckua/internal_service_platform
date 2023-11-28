from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """Basic model-workpiece"""

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Record info",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
