from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listings, WatchList

class BidForm(forms.Form):
    bid = forms.IntegerField()


class CreateForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ('title', 'price', 'description', 'link', 'image', 'category')
        lables = {
            'title': '',
            'price': '',
            'description': '',
            'link': '',
            'image': '',
            'category': '',
        }
        widgets = {
            'title': forms.TextInput(),
            'price': forms.NumberInput(),
            'description': forms.TextInput(),
            'link': forms.TextInput(),
        }



def index(request):
    try:
        listings = Listings.objects.all()
    except Listings.DoesNotExists:
        raise Http404("Listing not found")
    return render(request, "auctions/index.html", {
        'listings': listings
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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listings_view(request):
    return render(request, "auctions/listings.html", {
        'listings': Listings.objects.all()
    })

def unique_listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    author = listing.creator
    stopped = listing.is_open
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'is_author': author,
        'stopped': stopped,

    })


def create_listing(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            result = form.save(commit=False)
            result.creator = request.user
            result.save()
            listings = Listings.objects.all()
            return render(request, 'auctions/listings.html', {
                'listings': listings,
            })
    else:
        form = CreateForm()
        return render(request, 'auctions/create.html', {
            'form': form,
        })

def remove_from_watchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    if WatchList.objects.filter(user=request.user, listing=listing_id).exists():
        wl = WatchList.objects.get(listing=listing_id)
        wl.delete()
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'message': 'Removed from Watch List'
    })
    else:
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'message': 'Listing is not in Watch List'
        })

def add_to_watchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    if WatchList.objects.filter(user=request.user, listing=listing_id).exists():
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'message': 'Already added to Watch List',
        })
    user_list, created = WatchList.objects.get_or_create(user=request.user)
    user_list.listing.add(listing)
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'message': 'Added to watchlist'
    })

def watchlist(request):
    watchlist = WatchList.objects.all()
    wl = [_.listing.all for _ in watchlist]
    if wl:
        return render(request, 'auctions/watchlist.html', {
            'watchlist': wl[0]
        })
    else:
        return render(request, 'auctions/watchlist.html')


def bid(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    if request.method == 'POST':
        bid = BidForm(request.POST)
        if bid.is_valid():
            data = bid.cleaned_data.get('bid')
            if data <= listing.price:
                return render(request, 'auctions/listing.html', {
                    'listing': listing,
                    'message_bid': 'Bid must be greater than actual bid'
                })
            else:
                listing.price = data
                listing.save()
                return render(request, 'auctions/listing.html', {
                    'listing': listing,
                    'message_bid': 'Bid accepted'
                })
    else:
        bid = BidForm()
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'bid_form': bid
        })

def close_bid(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    if not listing.is_open:
        listing.is_open = True
        listing.save()
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'message_closed': 'Auction is stopped',

        })
    else:
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'message_closed': 'Auction is already stopped',

        })

