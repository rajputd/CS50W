from django import forms
from .models import AuctionListing, AuctionBid

class NewAuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

class NewBidForm(forms.ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['value', 'listing']
        widgets = {'listing': forms.HiddenInput()}