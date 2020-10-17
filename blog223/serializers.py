from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post'] 
        ref_name = 'blog223_comment' # mandatory for drf_yasg


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments'] 
        ref_name = 'blog223_post' # mandatory for drf_yasg



