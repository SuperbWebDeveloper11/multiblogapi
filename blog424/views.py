from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics
from .serializers import PostSerializer, CommentSerializer, PostlikeSerializer, CommentlikeSerializer
from .models import Post, Comment, Postlike, Commentlike
from .permissions import IsOwnerOrReadOnly, IsPostlikerOrReadOnly, IsCommentlikerOrReadOnly


# ***************** postviewset ***************** 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer): # add the post owner
        serializer.save(owner=self.request.user)
 

# ***************** commentviewset ***************** 
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.queryset.filter(post=current_post)

    def perform_create(self, serializer): # add the comment owner and post
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(owner=self.request.user, post=current_post)


# ***************** postlikeviewset ***************** 
class PostlikeViewSet(viewsets.ModelViewSet):
    queryset = Postlike.objects.all()
    serializer_class = PostlikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostlikerOrReadOnly]
    lookup_url_kwarg = 'postlike_pk'

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.queryset.filter(post=current_post)

    def perform_create(self, serializer): # add the comment owner and post
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(liked_by=self.request.user, post=current_post)


# ***************** commentlikeviewset ***************** 
class CommentlikeViewSet(viewsets.ModelViewSet):
    queryset = Commentlike.objects.all()
    serializer_class = CommentlikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentlikerOrReadOnly]
    lookup_url_kwarg = 'commentlike_pk'

    def get_queryset(self):
        current_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        return self.queryset.filter(comment=current_comment)

    def perform_create(self, serializer): # add the comment owner and post and comment
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        current_comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        serializer.save(liked_by=self.request.user, post=current_post, comment=current_comment)


