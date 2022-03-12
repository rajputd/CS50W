from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing
from .forms import NewAuctionListingForm


def index(request):
    listings = AuctionListing.objects.all()
    print(listings)
    return render(request, "auctions/index.html", { 'listings': listings })


@login_required
def create_listing(request):
    if request.method == "POST":
        submitted_form = NewAuctionListingForm(request.POST)

        if submitted_form.is_valid():
            print("saving new AuctionListing...")
            data = submitted_form.cleaned_data
            data['creator'] = request.user
            print(request.user)
            print(data)
            listing = AuctionListing.objects.create(**data)
            listing.save()
            # TODO return redirect('entry', title=title)
        else:
            print("Rejected new Auction Listing submission for some generic reason")
            return render(request, "auctions/create_listing.html", {'form': submitted_form})

    form = NewAuctionListingForm()
    return render(request, "auctions/create_listing.html", { 'form': form })


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
