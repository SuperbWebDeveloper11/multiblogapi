from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='blog321_posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='blog321_comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']


class Postlike(models.Model):
    post = models.ForeignKey(Post, related_name='postlikes', on_delete=models.CASCADE)
    liked_by = models.ForeignKey('auth.User', related_name='blog321_postlikes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "liked_by")
