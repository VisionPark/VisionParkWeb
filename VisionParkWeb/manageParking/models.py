from django.conf import settings
from django.db import models
from django.db.models import Count, Q

# https://www.youtube.com/watch?v=IEHOMF2Pukg&list=PLU8oAlHdN5BmfvwxFO7HdPciOCmmYneAB&index=12
# https://stackoverflow.com/questions/28712848/composite-primary-key-in-django
# https://stackoverflow.com/questions/34305805/django-foreignkeyuser-in-models
# https://docs.djangoproject.com/en/3.1/topics/db/models/#model-methods

class Parking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    canvas = models.JSONField(null=True)

    # Calculated fields
    @property
    def num_spaces(self):
        return self.space_set.count()
    
    @property
    def num_spaces_vacant(self):
        return Space.objects.filter(parking=self, vacant=True).count()
   
    def __str__(self):
        return f"{self.name} - {self.user}"


class Space(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    shortName = models.CharField(max_length=4)
    vacant = models.BooleanField(blank=True, null=True)
    since = models.DateTimeField(null=True)
    vertex = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shortName + " - " + str(self.parking)
