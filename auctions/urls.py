from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("close", views.close, name="close"),
    path("placecomment", views.placecomment, name="placecomment"),
    path("addwatchlist", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist", views.removewatchlist, name="removewatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path('categories', views.categories, name="categories"),
    path('categories/<str:category>', views.category, name="category")
]
