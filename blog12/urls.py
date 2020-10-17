from django.urls import include, path
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.PostViewSet)
router.register(r'(?P<pk>[^/.]+)/comments', views.CommentViewSet)
router.register(r'(?P<pk>[^/.]+)/estimations', views.EstimationViewSet)


urlpatterns = router.urls

# urlpatterns = format_suffix_patterns(urlpatterns)

