
## app description: 
this app allow post crud operations with concrete generic views 

## app features:
- unauthenticated uses have read only access
- users should be authenticated to add post
- only post owner who can edit or delete it


## models.py :

```python
class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog4_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, default='this post is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
```


## serializers.py :

```python
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner'] 
        ref_name = 'blog4_post' # mandatory for drf_yasg
```

## views.py :

```python
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # add the post owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

## urls.py :

```python
urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]
```
