from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint

# https://www.youtube.com/watch?v=IEHOMF2Pukg&list=PLU8oAlHdN5BmfvwxFO7HdPciOCmmYneAB&index=12
# https://stackoverflow.com/questions/28712848/composite-primary-key-in-django
# https://stackoverflow.com/questions/34305805/django-foreignkeyuser-in-models

class Parking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + str(self.user)


class Space(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    shortName = models.CharField(max_length=4)
    vacant = models.BooleanField(blank=True)
    since = models.DateTimeField()
    vertex = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shortName + " - " + str(self.parking)
