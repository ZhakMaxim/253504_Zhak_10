from django import forms
from .models import Review, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'text']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'age', 'password1', 'password2']