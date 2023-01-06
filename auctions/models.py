from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category


class Bid(models.Model):
    bid = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid}"


class Listing(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    image_url = models.CharField(max_length=512, blank=True)
    price = models.ForeignKey(Bid,  on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owened_items")
    watchlist = models.ManyToManyField(User, blank=True,related_name="watchlist")
    created_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    created_time = models.DateTimeField(default=datetime.now, blank=True)





