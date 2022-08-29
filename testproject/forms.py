from django.forms import ModelForm
from .models import User, Place, Rate
from django import forms
from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# User = get_user_model()


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


# class RatingForm(forms.ModelForm):
#     # rate = forms.NumberInput()
#     # user_id = forms.ChoiceField()
#     rate = forms.ModelChoiceField(
#         queryset=Rate.objects.all(),
#         to_field_name='rate',
#         required=False,
#         widget=forms.NumberInput(
#             attrs={
#             'type': 'range',
#             'step': '1',
#             'min': '1',
#             'max': '12',
#             'id': 'rate_range'
#         })
#     )

    # class Meta:
    #     model = Rate
    #     fields = '__all__'
