from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Place, Category, Favorite, Rate
from django.views import View, generic
from .forms import PlaceForm, CustomUserCreationForm, CustomUserUpdateForm
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import *


def navbar(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(context, 'navbar.html', context)


def home_page(request):
    return render(request, 'home.html')


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist yet")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def signup_user(request):
    form = CustomUserCreationForm()
    context = {'form': form}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something goes wrong')
    return render(request, 'login_register.html', context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    favorite_places = Favorite.objects.filter(user=user)
    context = {
        'user': user,
        'favorite_places': favorite_places,
    }
    return render(request, 'user_page.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = CustomUserUpdateForm(instance=user)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'update_user.html', context)


@login_required(login_url='login')
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('list_places')
    return render(request, 'delete_user.html')


# -------------------------------------------
def place_rating(pk):
    place_rate = Rate.objects.filter(place_id=pk)
    rate_amount = len(place_rate)
    rate_lst = [i.rate for i in place_rate]
    rating = int(sum(rate_lst) / len(rate_lst)) if rate_lst else 0

    return rating, rate_amount


def place_page(request, pk):
    place = Place.objects.get(id=pk)
    user_id = request.user.id
    try:
        user_rate = Rate.objects.get(user=user_id, place=place.id).rate
    except:
        user_rate = 0

    rating, rate_amount = place_rating(pk)

    lst_users_favorite_place = [i['user_id'] for i in Favorite.objects.filter(place_id=pk).values()]

    context = {'place': place,
               'user_rate': user_rate,
               'rating': rating,
               'rate_amount': rate_amount,
               'lst_users_favorite_place': lst_users_favorite_place
               }
    return render(request, 'place_page.html', context)


class PlaceView(View):
    place = None
    pass


class ListPlacesView(generic.ListView):
    model = Place
    context_object_name = 'list_places'
    template_name = 'list_places.html'

    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        return Place.objects.filter(
            Q(category__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    def get_context_data(self, **kwargs):
        context = super(ListPlacesView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# @login_required(login_url='login')
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


# ------------------------------------------

@login_required(login_url='login')
def user_rate(request):
    user_id = request.user.id
    place_id = request.POST.get('place_id')
    if request.method == 'POST':
        rate = request.POST.get('rate')
        Rate.objects.update_or_create(user_id=user_id, place_id=place_id, defaults={'rate': rate})

    return redirect('place', place_id)


@login_required(login_url='login')
def add_del_favorite(request):
    user_id = request.user.id
    place_id = request.POST.get('place_id')
    if request.method == 'POST':
        obj, created = Favorite.objects.get_or_create(user_id=user_id, place_id=place_id)
        if not created:
            obj.delete()

    return redirect('place', place_id)

