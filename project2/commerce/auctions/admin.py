from django.contrib import admin
from .models import AuctionListing, AuctionListingCategory, AuctionBid, Comment

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(AuctionListingCategory)
admin.site.register(AuctionBid)
admin.site.register(Comment)