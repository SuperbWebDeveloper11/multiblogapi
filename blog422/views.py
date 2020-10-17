from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, mixins
from .serializers import PostSerializer, CommentSerializer, PostlikeSerializer, CommentlikeSerializer
from .models import Post, Comment, Postlike, Commentlike
from .permissions import IsOwnerOrReadOnly, IsPostlikerOrReadOnly, IsCommentlikerOrReadOnly


# **************** post views ****************  
class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
                            
    def perform_create(self, serializer): # add the post owner
        serializer.save(owner=self.request.user)


class PostDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
                        
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# **************** comment views ****************  
class CommentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
                            
class CommentDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_pk' 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self): # filter comments by current_post
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Comment.objects.filter(post=current_post)
                        
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# **************** likeposts views ****************  
class PostlikeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = PostlikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_current_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_queryset(self): # filter comments by current_post
        current_post = self.get_current_post()
        return Postlike.objects.filter(post=current_post)

    def perform_create(self, serializer): # add comment owner and current post
        current_post = self.get_current_post()
        serializer.save(liked_by=self.request.user, post=current_post)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
                            
class PostlikeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = PostlikeSerializer
    lookup_url_kwarg = 'postlike_pk' 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostlikerOrReadOnly]

    def get_queryset(self): # filter comments by current_post
        current_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return Postlike.objects.filter(post=current_post)
                        
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# **************** likeposts views ****************  
class CommentlikeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CommentlikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_current_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_current_comment(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_pk'])

    def get_queryset(self): # filter comments by current_post
        current_post = self.get_current_post()
        current_comment = self.get_current_comment()
        return Commentlike.objects.filter(post=current_post, comment=current_comment)

    def perform_create(self, serializer): # add comment owner and current post
        current_post = self.get_current_post()
        current_comment = self.get_current_comment()
        serializer.save(liked_by=self.request.user, post=current_post, comment=current_comment)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
                            
class CommentlikeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = CommentlikeSerializer
    lookup_url_kwarg = 'commentike_pk' 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentlikerOrReadOnly]

    def get_current_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_current_comment(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_pk'])

    def get_queryset(self): # filter comments by current_post
        current_post = self.get_current_post()
        current_comment = self.get_current_comment()
        return Commentlike.objects.filter(post=current_post, comment=current_comment)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

