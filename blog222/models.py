from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='blog222_posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='blog222_comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

