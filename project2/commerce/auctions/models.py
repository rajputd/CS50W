from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # watchlist of listings?
    # list of created listings?
    # list of bids

    def __str__(self):
        return self.username

class AuctionListingCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(AuctionListingCategory, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id.__str__() + '-' + self.creator.__str__() + '-' + self.title

class AuctionBid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

# TODO auction listing
    # active
    # category

# TODO auction bid
    # auction listing
    # price
    # user

# TODO comments
    # listing
    # comments