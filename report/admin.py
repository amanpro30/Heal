from django.contrib import admin
from .models import Report, LabTest
from .models import Item
# Register your models here.
admin.site.register(Report)
admin.site.register(LabTest)
admin.site.register(Item)