from django.urls import path, re_path
from . import views
# from .views import PlaceView

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name="login"),
    path('place/<str:pk>/', views.place_page, name="place" ),
    path('place/list-places', views.list_places_page, name='list_places'),
    path('place/create-place', views.create_place, name='create_place'),
    path('place/place_form', views.place_form, name='place_form'),
    ]