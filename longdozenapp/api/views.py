from rest_framework import generics
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import PlaceSerializer
from longdozenapp.models import Place


class PlaceList(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id', )
    search_fields = ('name',)
