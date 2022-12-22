from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f'{self.username}'

class Category(models.Model):
    category = models.CharField(max_length=64,blank=True, null=True)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    active = models.BooleanField(default=True)
    bid = models.OneToOneField('bids', on_delete=models.CASCADE, related_name="list",blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    category = models.CharField(max_length=64 , blank=True, default="No Category")

    def __str__(self):
        return f"{self.title}"

class bids(models.Model):
    bid = models.FloatField()
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid",blank=True) 

    def __str__(self):
        return f"{self.bid}"


class comments(models.Model):
    comment = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usr_cmnt", blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True) 

    def __str__(self):
        return f"commented by '{self.user_id}' on ({self.listing})"
    
class watchList(models.Model):
    items = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s watchlist"

    