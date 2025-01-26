from django.contrib import admin
from .models import CarMake, CarModel


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'year', 'dealer_id']
    fields = ['name', 'type', 'year', 'dealer_id', 'car_make']


# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)
