from django.test import TestCase
from .models import Place


class PlaceModelTests(TestCase):
    def create_place(self):
        place_data = {
            'name': 'TestName',
            'description': 'TestDescription',
            'category': 'TestCategory',
            'location': 'TestLocation'
        }
        place = Place.objects.create(place_data)
        self.assertIs(place.save())
