from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name="home"),

    path('user/login', views.login_page, name="login"),
    path('user/logout', views.logout_user, name="logout"),
    path('user/register', views.signup_user, name='signup'),
    path('user/<str:pk>/', views.user_page, name="user_page"),
    path('user/user-update', views.update_user, name="update_user"),
    path('user/delete-user', views.delete_user, name='delete_user'),
    path('user_location/', views.user_location, name='user_location'),

    path('place/<str:pk>/', views.place_page, name="place"),
    path('place/', views.ListPlacesView.as_view(), name='list_places'),
    path('place/create-place', views.create_place, name='create_place'),
    path('place/update-place/<str:pk>/', views.update_place, name='update_place'),
    path('place/delete-place/<str:pk>/', views.delete_place, name='delete_place'),

    path('user_grade', views.user_grade, name='user_grade'),
    path('favorite', views.add_del_favorite, name='favorite'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
