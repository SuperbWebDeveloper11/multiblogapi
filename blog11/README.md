
## app description: 
this app allow post crud operations with concrete generic views 
comment crud operations with concrete generic views 
Estimatin crud operations with concrete generic views 


## app features:
- unauthenticated uses have full read only access
- users should be authenticated to add post or comment
- only post owner who can edit or delete it
- only comment owner who can edit or delete it
- a user could estimate a given post only one time


## models.py :

```python
class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog11_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, default='this post is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog11_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True, default='this comment is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Estimation(models.Model):
    ESTIMATION_CHOICES = (
            ('great', 'Great'),
            ('good', 'Good'),
            ('ok', 'Ok'),
            ('bad', 'Bad'),
            ('terrible', 'Terrible'),
            )
    post = models.ForeignKey(Post, related_name='estimations', on_delete=models.CASCADE)
    liked_by = models.ForeignKey('auth.User', related_name='blog11_estimations', on_delete=models.CASCADE)
    estimation = models.CharField(max_length=10, choices=ESTIMATION_CHOICES, blank=True)

    class Meta:
        unique_together = ("post", "liked_by")
```


## serializers.py :

```python
class EstimationSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Estimation
        fields = ['id', 'liked_by', 'post', 'estimation'] 
        ref_name = 'blog11_postlike' # mandatory for drf_yasg

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post'] 
        ref_name = 'blog11_comment' # mandatory for drf_yasg

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)
    estimations = EstimationSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'estimations'] 
        ref_name = 'blog11_post' # mandatory for drf_yasg
```

## views.py :

```python
# ***************** posts views ***************** 
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

# ***************** comments views ***************** 
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

# ***************** postlikes views ***************** 
class EstimationList(generics.ListCreateAPIView):
    serializer_class = EstimationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Estimation.objects.filter(post=current_post)

    # add the liked_by and post
    def perform_create(self, serializer):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(liked_by=self.request.user, post=current_post)

class EstimationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EstimationSerializer
    lookup_url_kwarg = 'estimation_pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEstimatorOrReadOnly]

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Estimation.objects.filter(post=current_post)
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
    # postlikes urls
    path('<int:pk>/estimations/', views.EstimationList.as_view()),
    path('<int:pk>/estimations/<int:estimation_pk>/', views.EstimationDetail.as_view()),
]

```
