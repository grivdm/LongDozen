
from django.contrib import admin
from django import forms
from .models import  Place, Category, Grade, Favorite
from leaflet.admin import LeafletGeoAdmin
from django.contrib.auth import get_user_model
User = get_user_model()
admin.site.register(Category)
admin.site.register(Grade)
admin.site.register(Favorite)
admin.site.register(User)


@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = ('id', 'name', 'location')