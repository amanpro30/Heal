from django.contrib import admin
from .models import AppointmentNurse, AppointmentPhysio
# Register your models here.
admin.site.register(AppointmentPhysio)
admin.site.register(AppointmentNurse)