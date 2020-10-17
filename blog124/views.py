from rest_framework import viewsets, permissions, generics
from .serializers import PostSerializer 
from .models import Post
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # add the post owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
 
