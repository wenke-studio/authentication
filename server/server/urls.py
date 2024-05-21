from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

api_info = openapi.Info(
    title="Wenke Studio API",
    default_version="v1",
    description="Full API for Wenke Studio",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="example@email.com"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    api_info,
    public=True,
    # permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger
    path(
        "swagger<format>/",
        SchemaView.without_ui(cache_timeout=0),
    ),
    path(
        "swagger/",
        SchemaView.with_ui("swagger", cache_timeout=0),
    ),
    path(
        "redoc/",
        SchemaView.with_ui("redoc", cache_timeout=0),
    ),
]
