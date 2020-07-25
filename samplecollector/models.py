from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from django.urls import reverse


# Create your models here.
class SampleCollector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Undisclosed'),
    )
    first_name = models.CharField(max_length=50)
    bike_available=models.BooleanField(default=True)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    profile_pic = models.ImageField(default='patient.png', upload_to='SampleCollector', blank=True, null=True)
    house_no = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin = models.IntegerField()
    gender = models.CharField(max_length=1, choices=gender_choices)
    dob = models.DateField()
    mob_no = models.BigIntegerField()
    
    def __str__(self):
        return f'{self.first_name}'



    
