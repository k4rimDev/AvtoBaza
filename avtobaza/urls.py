from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('akmin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/core/', include('apps.core.api.urls')),
    path('api/order/', include('apps.order.api.urls')),
    path('api/product/', include('apps.product.api.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Avto Baza",
        default_version='v1.0.0',
        description="E-commerce auto website",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="karimmirzaguliyev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
