from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly


# **************** post views ****************  
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer): # add post owner
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
                        

# **************** comment views ****************  
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_current_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_queryset(self): # filter comments by current_post
        current_post = self.get_current_post()
        return Comment.objects.filter(post=current_post)

    def perform_create(self, serializer): # add comment owner and current post
        current_post = self.get_current_post()
        serializer.save(owner=self.request.user, post=current_post)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_pk' 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self): # filter comments by current_post
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Comment.objects.filter(post=current_post)

