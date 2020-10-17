
## app description: 
this app allow post crud operations with concrete generic views 
comment crud operations with concrete generic views 


## app features:
- unauthenticated uses have full read only access
- users should be authenticated to add post or comment
- only post owner who can edit or delete it
- only comment owner who can edit or delete it


## models.py :

```python
class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog5_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, default='this post is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog5_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True, default='this comment is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

```


## serializers.py :

```python
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post'] 

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments'] 
        ref_name = 'blog5_post' # mandatory for drf_yasg
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

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Comment.objects.filter(post=current_post)

    # add the comment owner and post
    def perform_create(self, serializer):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(owner=self.request.user, post=current_post)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
       current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
       return Comment.objects.filter(post=current_post)
```

## urls.py :

```python
urlpatterns = [
    # posts urls
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    # comments urls
    path('<int:pk>/comments/', views.CommentList.as_view()),
    path('<int:pk>/comments/<int:comment_pk>/', views.CommentDetail.as_view()),
]
```
