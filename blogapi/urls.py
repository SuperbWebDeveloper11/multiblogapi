from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


# drf_yasg configuration
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# drf_yasg configuration
schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version='v1',
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
            ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        )



urlpatterns = [
    path('auth/', include('auth.urls')), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # login urls
    # path('blog10/', include('blog10.urls')), 
    # path('blog11/', include('blog11.urls')), 
    # path('blog12/', include('blog12.urls')), 

    path('blog121/', include('blog121.urls')), 
    path('blog122/', include('blog122.urls')), 
    path('blog123/', include('blog123.urls')), 
    path('blog124/', include('blog124.urls')), 
    path('blog221/', include('blog221.urls')), 
    path('blog222/', include('blog222.urls')), 
    path('blog223/', include('blog223.urls')), 
    path('blog224/', include('blog224.urls')), 
    path('blog321/', include('blog321.urls')), 
    path('blog322/', include('blog322.urls')), 
    path('blog323/', include('blog323.urls')), 
    path('blog324/', include('blog324.urls')), 
    path('blog421/', include('blog421.urls')), 
    path('blog422/', include('blog422.urls')), 
    path('blog423/', include('blog423.urls')), 
    path('blog424/', include('blog424.urls')), 

    path('admin/', admin.site.urls),

    # drf_yasg configuration
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),               
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),                         
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 

]

