from django.contrib import admin
from manageParking.models import Parking, Space

# Register your models here.

class SpaceAdmin(admin.ModelAdmin):
    list_filter=("parking_id",)
    readonly_fields = ('date_modified', 'date_created',)

class ParkingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_modified', 'date_created','num_spaces', 'num_spaces_vacant', 'num_spaces_not_vacant','num_spaces_unknown',)

admin.site.register(Parking, ParkingAdmin)
admin.site.register(Space, SpaceAdmin)