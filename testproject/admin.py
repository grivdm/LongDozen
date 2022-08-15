from django.contrib import admin
from .models import User, Place, Category
from leaflet.admin import LeafletGeoAdmin

admin.site.register(Category)

@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = ('id', 'name', 'location')

