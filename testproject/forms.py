from django.forms import ModelForm
from .models import Place
from django import forms

class PlaceForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Place name'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Place location'}))
    class Meta:
        model = Place
        fields = '__all__'
