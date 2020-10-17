from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics
from .serializers import PostSerializer, CommentSerializer, PostlikeSerializer
from .models import Post, Comment, Postlike
from .permissions import IsOwnerOrReadOnly, IsPostlikerOrReadOnly


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

    def perform_create(self, serializer): # add the comment owner and post
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

    def perform_create(self, serializer): # add the liked_by and post
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(liked_by=self.request.user, post=current_post)

class PostlikeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostlikeSerializer
    lookup_url_kwarg = 'postlike_pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostlikerOrReadOnly]

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Postlike.objects.filter(post=current_post)


