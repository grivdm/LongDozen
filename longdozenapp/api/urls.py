from django.urls import path
from . import views
from rest_framework import routers
from django.urls import include

router = routers.SimpleRouter()


router.register('place', viewset=views.PlaceViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),

]
