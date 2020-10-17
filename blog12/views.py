from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics
from .serializers import PostSerializer, CommentSerializer, EstimationSerializer
from .models import Post, Comment, Estimation
from .permissions import IsOwnerOrReadOnly, IsEstimatorOrReadOnly


# ***************** postviewset ***************** 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # add the post owner
    def perform_create(self, serializer):
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

    # add the comment owner and post
    def perform_create(self, serializer):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(owner=self.request.user, post=current_post)


# ***************** estimationviewset ***************** 
class EstimationViewSet(viewsets.ModelViewSet):
    queryset = Estimation.objects.all()
    serializer_class = EstimationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEstimatorOrReadOnly]
    lookup_url_kwarg = 'estimation_pk'

    def get_queryset(self):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.queryset.filter(post=current_post)

    # add the comment owner and post
    def perform_create(self, serializer):
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(liked_by=self.request.user, post=current_post)



