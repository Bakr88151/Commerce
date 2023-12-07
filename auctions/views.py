from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist
from .forms import Listing_form, Biding_form, comment_form

shopping_cart = "https://static.vecteezy.com/system/resources/previews/004/999/463/large_2x/shopping-cart-icon-illustration-free-vector.jpg"

def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all(),
        "shopping_cart_img" : shopping_cart,
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


def new(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "auctions/new.html",{
                "form" : Listing_form(),
            })
        else:
            form = Listing_form(request.POST)
            if form.is_valid():
                Listing.objects.create(title=form.cleaned_data["title"], description=form.cleaned_data["description"], image=form.cleaned_data["image"], base_price=form.cleaned_data["starting_bid"], poster=request.user, category=form.cleaned_data["category"])
                return HttpResponseRedirect(reverse("index"))
            else :
                return render(request, "auctions/new.html",{
                    "form" : Listing_form(),
                    "message": "make sure all inputs are valid",
            })
    else:
        return HttpResponseRedirect(reverse("login"))


def listing(request, listing_id):
    is_in_watchlist = False
    listing = Listing.objects.get(id=listing_id)
    user_watch_list = [item.listing for item in request.user.watchlist.all()]
    if listing in user_watch_list :
        is_in_watchlist = True
    current_user = request.user
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing" : Listing.objects.get(id=listing_id),
            "bid_form" : Biding_form,
            "shopping_cart_img" : shopping_cart,
            "comment_form" : comment_form,
            "comments" : Listing.objects.get(id=listing_id).comments.all(),
            "is_in_watchlist" : is_in_watchlist,
        })
    else:
        form = Biding_form(request.POST)
        listing = Listing.objects.get(id=listing_id)
        if form.is_valid() and request.user.is_authenticated and (listing.highest_bid is None or listing.highest_bid.value < form.cleaned_data["bid"] ) and listing.active:
            if listing.base_price <= form.cleaned_data['bid']:
                bid = Bid.objects.create(product=Listing.objects.get(id=listing_id), bidder=request.user, value=form.cleaned_data["bid"])
                listing.highest_bid = bid
                listing.save()
                bid_value = form.cleaned_data["bid"]
                return render(request, "auctions/listing.html", {
                    "listing" : Listing.objects.get(id=listing_id),
                    "bid_form" : Biding_form,
                    "shopping_cart_img" : shopping_cart,
                    "message" : f"Bid of ${format(bid_value, '.2f')} has been placed",
                    "comment_form" : comment_form,
                    "comments" : Listing.objects.get(id=listing_id).comments.all(),
                    "is_in_watchlist" : is_in_watchlist,
                })
        return render(request, "auctions/listing.html", {
            "listing" : Listing.objects.get(id=listing_id),
            "bid_form" : Biding_form,
            "shopping_cart_img" : shopping_cart,
            "message" : "make sure that the bid value is valid",
            "comment_form" : comment_form,
            "comments" : Listing.objects.get(id=listing_id).comments.all(),
            "is_in_watchlist" : is_in_watchlist,
        })


def close(request):
    listing = Listing.objects.get(id=request.POST.get("listing_id"))
    if listing.poster == request.user:
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id' : listing.id}))


def placecomment(request):
    form = comment_form(request.POST)
    if form.is_valid() and request.user.is_authenticated:
        listing = Listing.objects.get(id=request.POST.get("listing_id"))
        comment = Comment(comment=form.cleaned_data["comment"], poster=request.user)
        comment.save()
        listing.comments.add(comment)
        listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id" : listing.id}))


def addwatchlist(request):
    listing = Listing.objects.get(id=request.POST.get("listing_id"))
    wl = Watchlist(user=request.user, listing=listing)
    wl.save()
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id" : listing.id}))


def removewatchlist(request):
    request.user.watchlist.get(listing__id__contains=request.POST.get("listing_id")).delete()
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id" :request.POST.get("listing_id")}))


def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "watchlist" : request.user.watchlist.all(),
        "shopping_cart_img" : shopping_cart,
    })


def categories(request):
    categories_list = [item["category"] for item in Listing.objects.values("category").distinct() if item["category"] is not None]
    return render(request, 'auctions/categories.html',{
        "categories" : categories_list,
    })


def category(request, category):
    return render(request, 'auctions/category.html', {
        "listings" : Listing.objects.filter(category=category),
        "shopping_cart_img" : shopping_cart,
    })
