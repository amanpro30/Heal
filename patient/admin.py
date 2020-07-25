from django.contrib import admin
from .models import Patient, LabBooking

# Register your models here.
admin.site.register(Patient)
admin.site.register(LabBooking)
