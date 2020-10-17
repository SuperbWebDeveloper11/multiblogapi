from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner'] 
        ref_name = 'blog122_post' # mandatory for drf_yasg



