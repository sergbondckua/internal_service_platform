from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("search_keys.urls")),
    path("label/", include("labels_print.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("contract/", include("fill_in_docx.urls")),
]
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
