from django.urls import path, re_path
from . import views
# from .views import PlaceView

urlpatterns = [
    path('', views.home_page, name="home"),
    path('user/login', views.login_page, name="login"),
    path('user/logout', views.logoutUser, name="logout"),
    path('place/<str:pk>/', views.place_page, name="place"),
    path('place/list-places', views.list_places_page, name='list_places'),
    path('place/create-place', views.create_place, name='create_place'),
    path('place/update-place/<str:pk>/', views.update_place, name='update_place'),
    path('place/delete-place/<str:pk>/', views.delete_place, name='delete_place'),
    ]