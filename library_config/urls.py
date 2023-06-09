from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/users/", include("user.urls", namespace="user")),
    path("api/books/", include("books.urls", namespace="book")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/borrowings/", include("borrowings.urls", namespace="borrowing")),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
      ),
    path("admin/", admin.site.urls),
    path("api/users/", include("user.urls", namespace="users")),
    path('', include('payment.urls')),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
