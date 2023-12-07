from django import forms
from django.core.validators import MinValueValidator

class Listing_form(forms.Form):
    title = forms.CharField(required=True, max_length=256)
    description = forms.CharField(required=False, max_length=2046)
    starting_bid = forms.FloatField(required=True, min_value=0.01)
    category = forms.CharField(required=False, max_length=64)
    image = forms.URLField(required=False)

class Biding_form(forms.Form):
    bid = forms.FloatField(required=True, label="", widget=forms.NumberInput(attrs={"placeholder": "Bid"}))


class comment_form(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={"rows":"3"}))