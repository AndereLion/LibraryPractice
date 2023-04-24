from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
      ),
    path("admin/", admin.site.urls),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
