from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Place, Category
from django.views import View
from .forms import PlaceForm
from django.db.models import Q


from django.views import generic

def home_page(request):
    return render(request, 'home.html' )


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist yet")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    return render(request, 'login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def user_page(request):
    pass


def place_page(request, pk):
    place = Place.objects.get(id=pk)
    context = {'place': place}
    return render(request, 'place.html', context)


def list_places_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    places = Place.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    categories = Category.objects.all()

    context = {'places': places,
               'categories': categories
               }
    return render(request, 'list_places.html', context)


def create_place(request):
    form = PlaceForm()
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_places')
    context = {'form': form}
    return render(request, 'place_form.html', context)


def update_place(request, pk):
    place = Place.objects.get(id=pk)
    form = PlaceForm(instance=place)
    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return redirect('list_places')

    context = {'form': form}
    return render(request, 'place_form.html', context)

def delete_place(request, pk):
    place = Place.objects.get(id=pk)
    if request.method == 'POST':
        place.delete()
        return redirect('list_places')
    return render(request, 'delete_place.html')


def search_page(request):
    pass
