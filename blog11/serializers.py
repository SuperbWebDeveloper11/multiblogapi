from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator
from .models import Post, Comment, Estimation


class EstimationSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source='liked_by.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Estimation
        fields = ['id', 'liked_by', 'post', 'estimation'] 
        ref_name = 'blog11_postlike' # mandatory for drf_yasg


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post'] 
        ref_name = 'blog11_comment' # mandatory for drf_yasg


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)
    estimations = EstimationSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'estimations'] 
        ref_name = 'blog11_post' # mandatory for drf_yasg

