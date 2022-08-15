from django.forms import ModelForm
from .models import Place, Category
from django import forms
from leaflet.forms.widgets import LeafletWidget


class PlaceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Place name'}))
        self.name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Place name'}))
    class Meta:
        model = Place
        fields = ['name', 'description', 'category', 'location']
        widgets = {'location': LeafletWidget()}


