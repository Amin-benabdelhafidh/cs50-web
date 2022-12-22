from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createListing", views.create_auc, name="create_listing"),
    path("listing/<int:listing>", views.Listings, name="listing"),
    path("FilterByCategory", views.search, name="filter"),
    path("WatchList", views.Watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
