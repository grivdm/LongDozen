from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.
from .models import User, Place, Category

admin.site.register(User)
admin.site.register(Category)

@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
