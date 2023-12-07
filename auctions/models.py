from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    def __str__(self):
        return self.username


class Listing(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    poster = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    base_price = models.FloatField(blank=False)
    highest_bid = models.ForeignKey("Bid", default=None, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Bid(models.Model):
    product = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.value}: ({self.bidder})"


class Comment(models.Model):
    product = models.ManyToManyField(Listing, related_name="comments")
    poster = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=2046, default="")
    date = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name="watchlist", on_delete=models.CASCADE, default=None)