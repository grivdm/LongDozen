from django.forms import ModelForm
from .models import User, Place
from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']


class CustomUserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email']


class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'category', 'location']
        widgets = {'location': LeafletWidget()}