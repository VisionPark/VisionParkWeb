from django.contrib import admin
from manageParking.models import Parking, Space

# Register your models here.

class SpaceAdmin(admin.ModelAdmin):
    list_filter=("parking_id",)
    readonly_fields = ('date_modified', 'date_created',)

class ParkingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_modified', 'date_created',)

admin.site.register(Parking, ParkingAdmin)
admin.site.register(Space, SpaceAdmin)