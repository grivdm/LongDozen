from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Place, Category, Favorite, Grade
from django.views import generic
from .forms import PlaceForm, CustomUserCreationForm, CustomUserUpdateForm
from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Avg, Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin


def navbar(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(context, 'navbar.html', context)


def home_page(request):
    return render(request, 'home.html')


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
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
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
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


def user_location(request):
    if request.method == 'POST':
        request.session['latitude'] = request.POST.get('lat')
        request.session['longitude'] = request.POST.get('lng')
        request.session.save()
        return HttpResponse(status=200)

# -------------------------------------------


class PlacePageView(generic.DetailView):
    model = Place
    context_object_name = 'place'
    template_name = 'place_page.html'

    def get_queryset(self):
        latitude = self.request.session.get('latitude', 0)
        longitude = self.request.session.get('longitude', 0)
        user_spot = Point(float(longitude), float(latitude), srid=4326)
        return self.model.objects.annotate(
            rating=Avg('grades__grade'),
            grade_count=Count('grades__grade'),
            distance=Distance('location', user_spot)
        )

    def get_context_data(self, **kwargs):
        context = super(PlacePageView, self).get_context_data(**kwargs)
        try:
            context['user_grade'] = Grade.objects.get(user=self.request.user.id, place=self.object.id).grade
        except ObjectDoesNotExist:
            context['user_grade'] = 0
        context['is_favorite'] = Favorite.objects.filter(user=self.request.user.id, place=self.object.id).exists()
        return context


class ListPlacesView(generic.ListView):

    model = Place
    context_object_name = 'list_places'
    template_name = 'list_places.html'
    paginate_by = 10

    def get_queryset(self):
        latitude = self.request.session.get('latitude', 0)
        longitude = self.request.session.get('longitude', 0)
        user_spot = Point(float(longitude), float(latitude), srid=4326)
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        return Place.objects.filter(
            Q(category__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ).annotate(
            distance=Distance('location', user_spot),
            rating=Avg('grades__grade')
        ).order_by('distance')

    def get_context_data(self, **kwargs):
        context = super(ListPlacesView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['count_places'] = Place.objects.count()
        return context


class CreatePlaceView(LoginRequiredMixin, generic.CreateView):
    model = Place
    context_object_name = 'place'
    template_name = 'place_form.html'
    form_class = PlaceForm
    success_url = '/place'
    login_url = '/user/login'


class UpdatePlaceView(LoginRequiredMixin, generic.UpdateView):
    model = Place
    context_object_name = 'place'
    template_name = 'place_form.html'
    form_class = PlaceForm
    success_url = '/place'
    login_url = '/user/login'


class DeletePlaceView(LoginRequiredMixin, generic.DeleteView):
    model = Place
    success_url = '/place'
    template_name = 'delete_place.html'
    login_url = '/user/login'


# ------------------------------------------

@login_required(login_url='login')
def user_grade(request):
    user_id = request.user.id
    place_id = request.POST.get('place_id')
    if request.method == 'POST':
        grade = request.POST.get('grade')
        Grade.objects.update_or_create(user_id=user_id, place_id=place_id, defaults={'grade': grade})

    return redirect('place_page', place_id)


@login_required(login_url='login')
def add_del_favorite(request):
    user_id = request.user.id
    place_id = request.POST.get('place_id')
    if request.method == 'POST':
        obj, created = Favorite.objects.get_or_create(user_id=user_id, place_id=place_id)
        if not created:
            obj.delete()

    return redirect('place_page', place_id)
