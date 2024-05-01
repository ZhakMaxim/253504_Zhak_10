from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Review, User


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['name', 'rating', 'text']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'age', 'password1', 'password2']


class OrderForm(forms.Form):
    amount = forms.IntegerField(min_value=1)


class OrderDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(label='Confirm delete', required=True)


class PurchaseCreateForm(forms.Form):
    promo_code = forms.CharField(max_length=8, required=False)
    town = forms.CharField(max_length=50)


class PhoneNumberChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']