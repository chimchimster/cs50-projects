from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ All about User """


class Profile(models.Model):
    """ Model represents unique Profile with followers """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', null=True, blank=True)
    follows = models.ManyToManyField(User, related_name='follows', null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user} with {self.followers.count()} followers, follows {self.follows.count()}'

class Post(models.Model):
    """ Model which is responsible for each unique post that user creates """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    publishing_date = models.DateField(auto_now_add=True)
    edit_date = models.DateField(auto_now=True)
    text = models.CharField(max_length=1024)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'Post of {self.user}. Published: {self.publishing_date}. Edited: {self.edit_date}'

