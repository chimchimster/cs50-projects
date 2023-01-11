from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """" All about User"""

    followers_amount = models.IntegerField(default=0)
    followed_amount = models.IntegerField(default=0)

class Post(models.Model):
    """ Model which is responsible for each unique post that user creates """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    publishing_date = models.DateField(auto_now_add=True)
    edit_date = models.DateField(auto_now=True)
    text = models.CharField(max_length=1024)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'Post of {self.user}. Published: {self.publishing_date}. Edited: {self.edit_date}'

