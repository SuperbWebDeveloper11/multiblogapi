from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, mixins, status
from .serializers import PostSerializer, CommentSerializer, PostlikeSerializer, CommentlikeSerializer
from .models import Post, Comment, Postlike, Commentlike
from .permissions import IsOwnerOrReadOnly, IsPostlikerOrReadOnly, IsCommentlikerOrReadOnly


# **************** post views ****************  
class PostList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# **************** comment views ****************  
class CommentList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None):
        current_post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=current_post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        current_post = Post.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, post=current_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk, comment_pk):
        try:
            current_post = Post.objects.get(pk=pk)
            return Comment.objects.get(pk=comment_pk, post=current_post)
        except:
            raise Http404

    def get(self, request, pk, comment_pk, format=None):
        comment = self.get_object(pk, comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, comment_pk, format=None):
        comment = self.get_object(pk, comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk, format=None):
        comment = self.get_object(pk, comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# **************** postlike views ****************  
class PostlikeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None):
        current_post = Post.objects.get(pk=pk)
        comments = Postlike.objects.filter(post=current_post)
        serializer = PostlikeSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        current_post = Post.objects.get(pk=pk)
        serializer = PostlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(liked_by=self.request.user, post=current_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostlikeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostlikerOrReadOnly]

    def get_object(self, pk, postlike_pk):
        try:
            current_post = Post.objects.get(pk=pk)
            return Postlike.objects.get(pk=postlike_pk, post=current_post)
        except:
            raise Http404

    def get(self, request, pk, postlike_pk, format=None):
        postlike = self.get_object(pk, postlike_pk)
        serializer = PostlikeSerializer(postlike)
        return Response(serializer.data)

    def put(self, request, pk, postlike_pk, format=None):
        postlike = self.get_object(pk, postlike_pk)
        serializer = PostlikeSerializer(postlike, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, postlike_pk, format=None):
        postlike = self.get_object(pk, postlike_pk)
        postlike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# **************** commentlike views ****************  
class CommentlikeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk, comment_pk, format=None):
        current_post = Post.objects.get(pk=pk)
        current_comment = Comment.objects.get(pk=comment_pk, post=current_post)
        commentlikes = Commentlike.objects.filter(post=current_post, comment=current_comment)
        serializer = CommentlikeSerializer(commentlikes, many=True)
        return Response(serializer.data)

    def post(self, request, pk, comment_pk, format=None):
        current_post = Post.objects.get(pk=pk)
        current_comment = Comment.objects.get(pk=comment_pk, post=current_post)
        serializer = CommentlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(liked_by=self.request.user, post=current_post, comment=current_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentlikeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentlikerOrReadOnly]

    def get_object(self, pk, comment_pk, commentlike_pk):
        try:
            current_post = Post.objects.get(pk=pk)
            current_comment = Comment.objects.get(pk=comment_pk, post=current_post)
            return Commentlike.objects.get(pk=commentlike_pk, post=current_post, comment=current_comment)
        except:
            raise Http404

    def get(self, request, pk, comment_pk, commentlike_pk, format=None):
        commentlike = self.get_object(pk, comment_pk, commentlike_pk)
        serializer = PostlikeSerializer(commentlike)
        return Response(serializer.data)

    def put(self, request, pk, comment_pk, commentlike_pk, format=None):
        commentlike = self.get_object(pk, comment_pk, commentlike_pk)
        serializer = CommentlikeSerializer(commentlike, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk, commentlike_pk, format=None):
        commentlike = self.get_object(pk, comment_pk, commentlike_pk)
        commentlike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


