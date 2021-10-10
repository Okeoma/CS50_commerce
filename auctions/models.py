from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass	

class Categories(models.Model):
    categories = models.CharField(max_length=68)

    def __str__(self):
        return self.categories		
		
class Listing(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='auction')
    title = models.CharField(max_length=150)
    categories = models.ForeignKey('Categories', on_delete=models.CASCADE, default=1, related_name='categories_listing')
    description = models.TextField(max_length=500)   
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments_listing')
    starting_bid = models.IntegerField()    
    bids = models.ManyToManyField('Bid', related_name='bids_listing', blank=True)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, blank=True, null=True, related_name='last_bid_listing')
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    closed = models.BooleanField(default=False)
    
    def datepublished(self):
        return self.date.strftime('%B %d %Y')

    def __str__(self):
        return self.title		
		
class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    bid = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.bid)		
		
class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.user, self.date)


class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='personal_watchlist')
    listings = models.ManyToManyField('Listing', blank=True, related_name='watchlist_listings')

    def __str__(self):
        return 'Watchlist for %s' % (self.user)
