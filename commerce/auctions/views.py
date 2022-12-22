from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .models import User


def index(request):
    all_listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html", {
            "listings": all_listings ,
            'form': category_search()
    })

def search(request):
    if request.method == 'POST': 
        form = category_search(request.POST)
        if form.is_valid():
            filter = form.cleaned_data['search']
            return render(request, "auctions/filter.html", {
                'listings': Listing.objects.filter(category=filter),
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
                "username": username,
                "password": password
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
def create_auc(request):
    if request.method == "POST":
        name = request.POST["title"]
        des = request.POST['des']
        img = request.FILES["img"]
        b = request.POST['bid']
        u = User.objects.get(id=request.user.id)
        category = CreateListings(request.POST)
        if category.is_valid():
            cat = category.cleaned_data["category"]
            bi = bids(bid=b,user=u)
            bi.save()
            lis = Listing(title=name, description=des, image=img, user=u, bid=bi, category=cat)
            lis.save()

        return HttpResponseRedirect(reverse("listing", kwargs={'listing': lis.id}))
    else:
        return render(request, "auctions/createauction.html", {
            "cat": CreateListings(),
        })


@login_required
def Watchlist(request):
    wl = Listing.objects.filter(watchlist__user=request.user)
    return render(request, "auctions/watchlist.html", {
        "WL_items": wl,
        "length": len(wl),
    })


def Listings(request, listing):
    listi = Listing.objects.get(id=listing) 
    all_comments = comments.objects.filter(listing=listi)
    bid = listi.bid
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
    # ----bid part---- 
        if request.method == 'POST':
            if request.POST["form"] == "add-bid-form":
                d = float(request.POST["bid"])
                if d <= bid.bid:
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing": listing}))

                elif d > bid.bid:
                    bid.active = False
                    bid.save()
                    u = User.objects.get(id=user.id)
                    new = bids(user=u, bid=d)
                    new.save()
                    listi.bid = new
                    listi.save()
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing": listing}))
    # ----end of bid part----
    # ----comments part----
            elif request.POST["form"] == "comment-form":
                comment = Comment(request.POST)
                if comment.is_valid():
                    comnt = comment.cleaned_data['comment']
                    cmnt = comments(comment=comnt, user_id=user, listing=listi)
                    cmnt.save()
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing": listing}))
    # ----end comments part----
            elif request.POST["form"] == 'WatchList':
                try:
                    does_exist = watchList.objects.get(user=user, items=listi)
                    does_exist.delete()
                    return render(request, "auctions/listing.html", {
                        'listing': listi ,
                        'bid': bid ,
                        'comments': all_comments ,
                        'comment_form': Comment(),
                        'message': 'item deleted successfully'
                    })
                except ObjectDoesNotExist:
                    item_to_save = watchList(user=user, items=listi)
                    item_to_save.save()
                    return render(request, "auctions/listing.html", {
                        'listing': listi ,
                        'bid': bid ,
                        'comments': all_comments ,
                        'comment_form': Comment(),
                        "message1": 'item added successfully'
                    }) 
    return render(request, "auctions/listing.html", {
        'listing': listi ,
        'bid': bid ,
        'comments': all_comments ,
        'comment_form': Comment(),
        "message2": 'you should login or signup to be able to make bids or to add this item to watchlist'
        })