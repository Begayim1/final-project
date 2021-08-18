from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


from account.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    discription = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='reply-images')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15] + '...'

    class Meta:
        ordering = ('-created', )


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user} -- {self.post}"
