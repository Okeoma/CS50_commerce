from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

def index(request):
    listings = Listing.objects.all().order_by('id').reverse()    
    categories = Categories.objects.all()
    user = request.user
    if user.id is None:
	    return render(request, "auctions/index.html",{       
            'listings': listings,           
			'categories' : categories,
			'title': 'Active Listings'
        })
        
    watchlist = Watchlist.objects.get(user=request.user)
    sum_listing = watchlist.listings.count()
    return render(request, "auctions/index.html", {
        'listings': listings,
        'sum_listing': sum_listing,
        'watchlist': watchlist,        
		'categories' : categories,
		'title': 'Active Listings'
		
    })
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
				'title': 'Login'
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html", {
		    'title': 'Login'
		})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
				'title': 'Register'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            watchlist = Watchlist.objects.create(user=user)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
				'title': 'Register'
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/register.html", {
		    'title': 'Register'
		})
		
def categories(request, categories):    
    category_name = Categories.objects.get(categories=categories)
    listings = Listing.objects.filter(categories=category_name).order_by('id').reverse() 	
    categories = Categories.objects.all()
    user = request.user
	
    if user.id is None:
        return render(request, "auctions/index.html")    
    watchlist = Watchlist.objects.get(user=request.user)
    sum_listing = watchlist.listings.count()   
       
    return render(request, "auctions/categories.html", {
	    'title': category_name,
        'listings': listings,
		'sum_listing': sum_listing,        
		'categories': categories
        
    })

def my_watchlist(request):  
    categories = Categories.objects.all()  
    if request.user.id is None:
        return HttpResponseRedirect(reverse("index"))

    watchlist = Watchlist.objects.get(user=request.user)
    sum_listing = watchlist.listings.count()
    return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist,        
        'sum_listing': sum_listing,
		'categories' : categories,
		'title': 'My Watchlist'
    })
	
def listing_view(request, listing):
    if request.method == 'GET':        
        categories= Categories.objects.all()
        if request.user.id is None:
            return HttpResponseRedirect(reverse("login"))

        watchlist = Watchlist.objects.get(user=request.user)
        sum_listing = watchlist.listings.count()
        listing = Listing.objects.get(id=listing)
        comments = listing.comments.all().order_by('id').reverse()
        return render(request, 'auctions/listing_view.html', {
            'listing': listing,
            'watchlist': watchlist,
            'categories': categories,			
            'comments': comments,
            'sum_listing':sum_listing,
			'title': 'Listing Status'
        })        

def bid_to_listing(request, listing):
    if request.method == 'POST':
        listing_to_add = Listing.objects.get(id=listing)
        total_bid = request.POST['totalBid']
        bid = Bid.objects.create(user=request.user, listing=listing_to_add, bid=total_bid)
        listing_to_add.bids.add(bid)
        listing_to_add.last_bid = bid
        listing_to_add.save()
        return HttpResponse('success')
		
def add_to_watchlist(request, listing):
    if request.method == 'POST':
        listing_to_add = Listing.objects.get(id=listing)
        watchlist = Watchlist.objects.get(user=request.user)
        if listing_to_add in watchlist.listings.all():
            watchlist.listings.remove(listing_to_add)
            watchlist.save()
        else:
            watchlist.listings.add(listing_to_add)
            watchlist.save()
        return HttpResponse('success')		

def delete_listing_from_watchlist(request, listing):    
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing)
        watchlist = Watchlist.objects.get(user=request.user)
        watchlist.listings.remove(listing)
        watchlist.save()        
        return HttpResponse('success')
		
def close_listing(request, listing):
    if request.method == 'GET':
        listing_item = Listing.objects.get(id=listing)
        listing_item.closed = True
        listing_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def add_comment(request, listing):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing)
        comment = request.POST['comment']
        if not comment:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        comment = Comment.objects.create(comment=comment, user=request.user)
        listing.comments.add(comment)
        listing.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		
def delete_comment(request, comment):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment)
        comment.delete()
        return HttpResponse('success')
		
def my_listings(request, user):
    user_listing = User.objects.get(username=user)
    categories= Categories.objects.all()
    listings = Listing.objects.filter(user=user_listing)
    watchlist = Watchlist.objects.get(user=request.user)
    sum_listing = watchlist.listings.count()

    if request.user.username != user:
        return redirect('my_listings', user=request.user.username)

    return render(request, "auctions/my_listings.html", {
        'listings': listings,
        'watchlist': watchlist,
        'sum_listing': sum_listing,
		'categories': categories,
		'title': 'My Listings'
    })


def add_listing(request):
    categories = Categories.objects.all()    
    user = request.user
	
    if user.id is None:
        return redirect('login')
    watchlist = Watchlist.objects.get(user=request.user)
    sum_listing = watchlist.listings.count()

    if request.method == 'GET':
        return render(request, "auctions/add_listings.html", {
            'form': ListingForm(),
            'sum_listing': sum_listing,            
			'categories': categories,
			'title': 'Add Listing'
        })		
    else:
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            categories = form.cleaned_data['categories']            
            image = form.cleaned_data['image']

            auctionCreated = Listing.objects.create(
                user=request.user,
                title=title,
                description=description,
                starting_bid=starting_bid,
                categories=categories,                
                image=image
            )
            return HttpResponseRedirect(reverse("index"))
			
			
def my_winnings(request):
    listings = Listing.objects.all().order_by('id').reverse()
    categories = Categories.objects.all()	
    user = request.user
    if request.user.id is None:
        return HttpResponseRedirect(reverse("index"))
    
    watchlist = Watchlist.objects.get(user=request.user)
    sum_listing = watchlist.listings.count()
    return render(request, "auctions/my_winnings.html", {
        'listings': listings,
        'watchlist': watchlist,
        'sum_listing': sum_listing,
        'categories': categories,
		'title': 'My Winnings'
    })
	
	
class ListingForm(forms.ModelForm):
    """Image Model Form for processing images"""
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'categories', 'image')
        widgets = {'categories' : forms.Select(choices=Categories.objects.all(), attrs={'class' : 'form-control'}),                   
                   'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'starting_bid': forms.NumberInput(attrs={'class': 'form-control'})} 

    