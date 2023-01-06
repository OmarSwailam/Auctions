from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib import messages
from .forms import *


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
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
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            price = form.cleaned_data["price"]
            bid = Bid(bid=price, bidder=request.user)
            bid.save()
            category = form.cleaned_data["categories"]
            category_object = Category.objects.get(category=category)
            owner = request.user
            newlisting = Listing(title=title, description=description,
                        image_url=image_url, price=bid,
                        category=category_object,
                        owner=owner)
            newlisting.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/createListing.html", {
                "form": form
            })

    return render(request, "auctions/createListing.html", {
        "form": CreateListingForm(initial={'categories': Category.objects.get(category="No Category")})
    })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    is_in_watchlist = request.user in listing.watchlist.all()
    comments = listing.comment_set.all()
    if listing.is_active == False:
        bid_winner = listing.price.bidder
    else:
        bid_winner = ""
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "bid_winner": bid_winner

    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def category(request, category_name):
    category = Category.objects.get(category=category_name)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings
    })



@login_required
def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def add(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))

@login_required
def remove(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))

@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    content = request.POST["comment"]
    comment = Comment(user=request.user, content=content, listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_bid = float(request.POST["bid"])
    if user_bid > listing.price.bid:
        bid = Bid(bid=user_bid, bidder=request.user)
        bid.save()
        Listing.objects.filter(pk=listing_id).update(price=bid)
        messages.success(request, "Success." )
        return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))
    else:
        messages.warning(request, "Failed")
        return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.filter(pk=listing_id)
    listing.update(is_active=False)
    return HttpResponseRedirect(reverse("listing", kwargs={
        "listing_id": listing_id
    }))


