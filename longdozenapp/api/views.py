from rest_framework import generics, viewsets
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import PlaceSerializer
from longdozenapp.models import Place
#
#
# class PlaceList(generics.ListAPIView):
#     queryset = Place.objects.all()
#     serializer_class = PlaceSerializer
#     filter_backends = (DjangoFilterBackend, SearchFilter)
#     filterset_fields = ('id', )
#     search_fields = ('name',)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['name', ]
    search_fields = ['name', 'category']

    def get_queryset(self):
        category_filter = self.request.query_params.get('category', None)
        if category_filter is None:
            return super().get_queryset()
        queryset = Place.objects.all()
        category_id = category_filter
        if category_id.isnumeric():
            return queryset.filter(category_id=category_id)
