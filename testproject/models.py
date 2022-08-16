from django.contrib.gis.db import models as models_gis
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    avatar = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
        default='images/def_avatar.jpg'
    )


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Place(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location = models_gis.PointField()

    class Meta:
        ordering = ['-name']


    def __str__(self):
        return self.name


class Favorite(models.Model):
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Rate(models.Model):
    log_time = models.TimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()

