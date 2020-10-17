
## app description: 
this app allow post crud operations with concrete generic views 
comment crud operations with concrete generic views 
Postlike crud operations with concrete generic views 
Commentlike crud operations with concrete generic views 


## app features:
- unauthenticated uses have full read only access
- users should be authenticated to add post or comment
- only post owner who can edit or delete it
- only comment owner who can edit or delete it
- a user could like a given post only one time


## models.py :

```python
class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog9_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, default='this post is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog9_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True, default='this comment is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Postlike(models.Model):
    post = models.ForeignKey(Post, related_name='postlikes', on_delete=models.CASCADE)
    liked_by = models.ForeignKey('auth.User', related_name='blog9_postlikes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "liked_by")

class Commentlike(models.Model):
    post = models.ForeignKey(Post, related_name='commentlikes', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='commentlikes', on_delete=models.CASCADE)
    liked_by = models.ForeignKey('auth.User', related_name='blog9_commentlikes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "comment", "liked_by")

```


## serializers.py :


```python
class CommentlikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    post = serializers.ReadOnlyField(source='post.title')
    comment = serializers.ReadOnlyField(source='comment.body')

    class Meta:
        model = Commentlike
        fields = ['id', 'liked_by', 'post', 'comment'] 
        ref_name = 'blog9_postlike' # mandatory for drf_yasg

class PostlikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Postlike
        fields = ['id', 'liked_by', 'post'] 
        ref_name = 'blog9_postlike' # mandatory for drf_yasg

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.title')
    commentlikes = CommentlikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post', 'commentlikes'] 
        ref_name = 'blog9_comment' # mandatory for drf_yasg

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)
    postlikes = PostlikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'postlikes'] 
        ref_name = 'blog9_post' # mandatory for drf_yasg
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
class PostlikeList(generics.ListCreateAPIView):
    serializer_class = PostlikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Postlike.objects.filter(post=current_post)

    # add the liked_by and post
    def perform_create(self, serializer):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(liked_by=self.request.user, post=current_post)

class PostlikeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostlikeSerializer
    lookup_url_kwarg = 'postlike_pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostlikerOrReadOnly]

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Postlike.objects.filter(post=current_post)

# ***************** commentlikes views ***************** 
class CommentlikeList(generics.ListCreateAPIView):
    serializer_class = CommentlikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        current_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        return Commentlike.objects.filter(comment=current_comment)

    # add the liked_by and post and comment
    def perform_create(self, serializer):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        serializer.save(liked_by=self.request.user, post=current_post, comment=current_comment)

class CommentlikeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentlikeSerializer
    lookup_url_kwarg = 'commentlike_pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostlikerOrReadOnly]

    def get_queryset(self):
        current_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        return Commentlike.objects.filter(comment=current_comment)

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
    path('<int:pk>/postlikes/', views.PostlikeList.as_view()),
    path('<int:pk>/postlikes/<int:postlike_pk>/', views.PostlikeDetail.as_view()),
    # commentlikes urls
    path('<int:pk>/comments/<int:comment_pk>/commentlikes/', views.CommentlikeList.as_view()),
    path('<int:pk>/comments/<int:comment_pk>/commentlikes/<int:commentlike_pk>/', views.CommentlikeDetail.as_view()),
]

```
