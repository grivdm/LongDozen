from django import forms
from .models import User, Place
from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control my-5'})
        }


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place

        fields = ['name', 'description', 'category', 'location']
        widgets = {
            'location': LeafletWidget()
        }