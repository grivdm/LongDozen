from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Place
from django.views import View
from .forms import PlaceForm
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

def create_place(request):
    form = PlaceForm
    if request.method == 'POST':
        print(request.POST)
    context = {'form': form}
    return render(request, 'place_form.html', context)

# class PlaceView(View):
#     template_name = 'list_places.html'
#     form_class = PlaceForm
#
#     def get(self, request,  *args, **kwargs):
#         form = self.form_class
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('home'))
#         else:
#             return render(request, self.template_name, {'form': form})

# class PlaceView(generic.ListView):
#     model = Place
#     queryset = Place.objects.all()
#     context = {'places': queryset}

def search_page(request):
    pass
