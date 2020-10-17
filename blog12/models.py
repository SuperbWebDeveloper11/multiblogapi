from django.db import models


class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog12_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, default='this post is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blog12_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True, default='this comment is empty')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Estimation(models.Model):
    ESTIMATION_CHOICES = (
            ('great', 'Great'),
            ('good', 'Good'),
            ('ok', 'Ok'),
            ('bad', 'Bad'),
            ('terrible', 'Terrible'),
            )
    post = models.ForeignKey(Post, related_name='estimations', on_delete=models.CASCADE)
    liked_by = models.ForeignKey('auth.User', related_name='blog12_estimations', on_delete=models.CASCADE)
    estimation = models.CharField(max_length=10, choices=ESTIMATION_CHOICES, blank=True)

    class Meta:
        unique_together = ("post", "liked_by")
