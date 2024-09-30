# rentals/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Rental


class RentalForm(forms.Form):
    """
    Form to initiate a new rental.
    """
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Student")
    book_title = forms.CharField(max_length=255, label="Book Title")


class ExtendRentalForm(forms.Form):
    """
    Form to extend an existing rental.
    """
    rental = forms.ModelChoiceField(queryset=Rental.objects.all(), label="Select Rental")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rental'].queryset = Rental.objects.all()
