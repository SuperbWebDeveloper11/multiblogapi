from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Post, Comment, Postlike, Commentlike


class CommentlikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    post = serializers.ReadOnlyField(source='post.title')
    comment = serializers.ReadOnlyField(source='comment.body')

    class Meta:
        model = Commentlike
        fields = ['id', 'liked_by', 'post', 'comment'] 
        ref_name = 'blog424_postlike' # mandatory for drf_yasg


class PostlikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Postlike
        fields = ['id', 'liked_by', 'post'] 
        ref_name = 'blog424_postlike' # mandatory for drf_yasg


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.title')
    commentlikes = CommentlikeSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post', 'commentlikes'] 
        ref_name = 'blog424_comment' # mandatory for drf_yasg


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)
    postlikes = PostlikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'postlikes'] 
        ref_name = 'blog424_post' # mandatory for drf_yasg

