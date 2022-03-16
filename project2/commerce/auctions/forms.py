from django import forms
from .models import AuctionListing, AuctionBid, Comment

class NewAuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

class NewBidForm(forms.ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['value', 'listing']
        widgets = {'listing': forms.HiddenInput()}

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'listing']
        widgets = {'listing': forms.HiddenInput()}