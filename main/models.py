from django.conf import settings
from django.contrib.auth.models import User
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


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда', related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Продукт', related_name='ratings')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.star} - {self.post}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"




class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user} -- {self.post}"

















