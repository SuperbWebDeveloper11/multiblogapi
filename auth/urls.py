from django.urls import path, include
from rest_framework import routers 
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # other urls
]

urlpatterns += router.urls

# urlpatterns = format_suffix_patterns(urlpatterns)

