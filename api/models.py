from datetime import date
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_request = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=2000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, through='Like')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_date = models.DateField(default=date.today)
