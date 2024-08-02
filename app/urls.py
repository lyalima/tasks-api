from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Task Management API",
      default_version='v1',
      description="API for task management.",
      terms_of_service="",
      contact=openapi.Contact(email="lyalima0328@gmail.com"),
      license=openapi.License(name=""),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('tasks.urls')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
