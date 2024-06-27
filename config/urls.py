from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from chat.views import FirstPanel

schema_view = get_schema_view(
    openapi.Info(
        title="Chat API",
        default_version="v1",
        description="Chat project api",
        terms_of_services="CHAT"
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),



    # swagger
    path('swagger/', schema_view.with_ui(
        "swagger", cache_timeout=0), name="swagger-swagger-ui"),
    path('redoc/', schema_view.with_ui(
        "redoc", cache_timeout=0), name="schema-redoc"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)