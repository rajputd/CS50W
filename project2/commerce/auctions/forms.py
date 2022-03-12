from django import forms
from .models import AuctionListing

class NewAuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url']