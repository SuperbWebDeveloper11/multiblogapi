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
    path('<int:pk>/postlikes/', views.PostlikeList.as_view()),
    path('<int:pk>/postlikes/<int:postlike_pk>/', views.PostlikeDetail.as_view()),
    # commentlikes urls
    path('<int:pk>/comments/<int:comment_pk>/commentlikes/', views.CommentlikeList.as_view()),
    path('<int:pk>/comments/<int:comment_pk>/commentlikes/<int:commentlike_pk>/', views.CommentlikeDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

