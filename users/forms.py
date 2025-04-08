from django import forms
from .models import Address, Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','street', 'city', 'state', 'zipcode']
