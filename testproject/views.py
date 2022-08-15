from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Place
from django.views import View
from .forms import PlaceForm
from django.contrib.gis.geos import Point
# Create your views here.

from django.views import generic

def home_page(request):
    return render(request, 'home.html' )


def login_page(request):
    return HttpResponse('LogIN')


def user_page(request):
    pass


def place_page(request, pk):
    place= Place.objects.get(id=pk)

    context = {'place': place}
    return render(request, 'place.html', context)


def list_places_page(request):
    places = Place.objects.all()
    context = {'places': places}
    return render(request, 'list_places.html', context)


def place_form(request):
    form = PlaceForm()
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
    context = {'form': form}
    return render(request, 'place_form.html', context)


def create_place(request):
    form = PlaceForm()
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
    return render(request, 'place_form.html')



def search_page(request):
    pass
