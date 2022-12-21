from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass


CATEGORIES = [
    ('ART', 'Art'),
    ('HOUSE', 'House'),
    ('PETS', 'Pets'),
    ('JOY', 'Joy')
]


class Listings(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=64, default='')
    description = models.CharField(max_length=300, default='')
    price = models.IntegerField(default='')
    link = models.CharField(max_length=128, default='')
    image = models.ImageField(upload_to='images/', default='', null=True, blank=True)
    is_open = models.BooleanField(default=False)
    category = models.CharField(
        max_length=5,
        choices=CATEGORIES,
        default='Art',
    )

    def __str__(self):
        return f'Name: {self.title}, price: {self.price}'


class WatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listings)

    def __str__(self):
        return f'WatchList of the {self.user}'


class Bids(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, default='')

    def __str__(self):
        return f'Bids of the {self.user}'
