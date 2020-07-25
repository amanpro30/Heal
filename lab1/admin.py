from django.contrib import admin
from .models import Lab1, LabSlot1, BookingDateLab, Test1

# Register your models here.
admin.site.register(Lab1)
admin.site.register(LabSlot1)
admin.site.register(BookingDateLab)
admin.site.register(Test1)

# admin.site.register(AppointmentPhysiotherapist)