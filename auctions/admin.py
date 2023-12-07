from django.contrib import admin
from .models import Listing, User, Bid, Comment, Watchlist

# Register your models here.

class Bid_admin(admin.ModelAdmin):
    list_display = ("product", "bidder", "value", "date")


class Listing_admin(admin.ModelAdmin):
    list_display = ("title", "poster", "highest_bid")


class Watchlist_admin(admin.ModelAdmin):
    list_display = ("user", "listing")

admin.site.register(Listing, Listing_admin)
admin.site.register(User)
admin.site.register(Bid, Bid_admin)
admin.site.register(Comment)
admin.site.register(Watchlist)
