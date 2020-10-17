from django.urls import include, path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    # posts urls
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    # comments urls
    path('<int:pk>/comments/', views.CommentList.as_view()),
    path('<int:pk>/comments/<int:comment_pk>/', views.CommentDetail.as_view()),
    # postlikes urls
    path('<int:pk>/estimations/', views.EstimationList.as_view()),
    path('<int:pk>/estimations/<int:estimation_pk>/', views.EstimationDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

