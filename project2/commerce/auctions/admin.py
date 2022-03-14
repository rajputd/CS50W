from django.contrib import admin
from .models import AuctionListing, AuctionListingCategory

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(AuctionListingCategory)