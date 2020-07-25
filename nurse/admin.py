from django.contrib import admin
from .models import Nurse, Slot, BookingDate

# Register your models here.
admin.site.register(Nurse)
admin.site.register(Slot)
admin.site.register(BookingDate)
