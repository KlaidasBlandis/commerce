from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name="owner")
    image = models.URLField(blank=True)
    category = models.CharField(max_length=50)
    last_bid = models.IntegerField(blank=True, default=None, null=True)
    bidder = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    status = models.BooleanField(default=True)

class Watchlist(models.Model):
    wlister = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name="wlister")
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.URLField(blank=True, default=None)
    category = models.CharField(max_length=50)
    last_bid = models.IntegerField(blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, default=None)
    comment = models.CharField(max_length=1000)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)

class Bids(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, null=True)