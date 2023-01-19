from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """ All about User """


class Profile(models.Model):
    """ Model represents unique Profile with followers """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Username")
    followers = models.ManyToManyField(User, related_name='followers', null=True, blank=True, verbose_name="Followers")
    follows = models.ManyToManyField(User, related_name='follows', null=True, blank=True, verbose_name="Followed")

    def __str__(self):
        return f'Profile of {self.user}'

    class Meta:
        verbose_name = "User's Profile"
        verbose_name_plural = "User's Profile"
        ordering = ['id']


class Post(models.Model):
    """ Model which is responsible for each unique post that user creates """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Username")
    publishing_date = models.DateField(auto_now_add=True, verbose_name="Published at")
    edit_date = models.DateField(auto_now=True, verbose_name="Edited at")
    text = models.CharField(max_length=1024, verbose_name="Content")
    likes = models.IntegerField(default=0, verbose_name="Quantity of likes")

    def __str__(self):
        return f'Post of {self.user}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publishing_date']

