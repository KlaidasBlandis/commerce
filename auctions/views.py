from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse


from .models import Comments, User, AuctionListings, Watchlist

def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListings.objects.all()
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

@login_required
def create(request):
    categories = ["Fashion", "Toys", "Electronics", "Home", "Sports", "Health & Beauty", "Deals", "Others"]
    if request.method == "POST":
        owner = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        if 'category' in request.POST:
            category = request.POST["category"]
        else:
            category = False

        if title != None and description != None and price != None:
            l = AuctionListings(title=title, description=description, owner=owner, price=price, image=image, category=category)
            l.save()
            return render(request, "auctions/index.html", {
                "listings": AuctionListings.objects.all()
            })
        else:
            return render(request, "auctions/error.html", {
                "message": "Not all the necessary spaces are filled."
            })
    else:
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    
def listing(request, list_id):
    l = AuctionListings.objects.get(pk=list_id)
    
    return render(request, "auctions/listing.html", {
        "l": l,
        "comments": Comments.objects.all()
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        listing = request.POST["listing"]
        wlister = request.user
        l = AuctionListings.objects.get(id=listing)
        wl = Watchlist(wlister=wlister, title=l.title, description=l.description, price=l.price, image=l.image, category=l.category, last_bid=l.last_bid)
        wl.save()
        return render(request, "auctions/watchlist.html", {
            "listings": Watchlist.objects.all()
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "listings": Watchlist.objects.all()
        })

@login_required
def remove_wl(request):
    listing = request.GET["watchlist"]
    Watchlist.objects.filter(pk=listing).delete()
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlist.objects.all()
    })

@login_required
def bid(request):
    bid = int(request.GET["bid"])
    bidder = request.user
    listing_id = request.GET["listing"]
    listing = AuctionListings.objects.get(pk=listing_id)
    if listing.last_bid is not None:
        if bid > listing.last_bid:
            new_listing = AuctionListings.objects.filter(pk=listing_id).update(last_bid=bid, bidder=bidder)
            return HttpResponseRedirect(reverse("listing", kwargs={'list_id': listing_id}))
        else:
            return render(request, "auctions/error.html", {
                "message": "The bid is too small"
            })
    else:
        if bid >= listing.price:
            new_listing = AuctionListings.objects.filter(pk=listing_id).update(last_bid=bid, bidder=bidder)
            return HttpResponseRedirect(reverse("listing", kwargs={'list_id': listing_id}))
        else:
            return render(request, "auctions/error.html", {
                "message": "The bid is too small"
            })

@login_required
def close(request):
    listing_id = request.GET["listing"]
    AuctionListings.objects.filter(pk=listing_id).update(status=False)
    return HttpResponseRedirect(reverse("listing", kwargs={'list_id': listing_id}))

@login_required
def comment(request):
    comment = request.POST["comment"]
    user = request.user
    listing_id = request.POST["listing"]
    listing = AuctionListings.objects.get(pk=listing_id)
    k = Comments(user=user, comment=comment, listing=listing)
    k.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'list_id': listing_id}))

def categories(request):
    categories = ["Fashion", "Toys", "Electronics", "Home", "Sports", "Health & Beauty", "Deals", "Others"]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    listings = AuctionListings.objects.filter(category=category).all()
    return render(request, "auctions/cat_listings.html", {
        "listings": listings,
        "category": category
    })
