from django.contrib import admin
from manageParking.models import Parking, Space

# Register your models here.

class SpaceAdmin(admin.ModelAdmin):
    list_filter=("parking_id",)

admin.site.register(Parking)
admin.site.register(Space, SpaceAdmin)