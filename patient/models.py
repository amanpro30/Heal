from django.db import models
from django.contrib.auth.models import User
from lab1.models import Test1, Lab1
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from django.urls import reverse
from samplecollector.models import SampleCollector
from tests.models import Test
from report.models import Report

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Undisclosed'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    profile_photo = models.ImageField(default='patient.png', upload_to='Patient_pics', blank=True)
    house_no = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin = models.IntegerField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    dob = models.DateField()
    mob_no = models.BigIntegerField()
    
    def __str__(self):
        return f'{self.first_name}'



class LabBooking(models.Model):
    date=models.DateField(default=datetime.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(Lab1, on_delete=models.CASCADE, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    collector=models.ForeignKey(SampleCollector, on_delete=models.CASCADE, null=True,blank=True)
    status_choices = (
        ('Booked', 'Booked'),
        ('Sampled', 'Sampled'),
        ('Collected', 'Collected'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=status_choices)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('lab1:select_collector', kwargs={'pk':self.pk})
    
    

    
      

    

    



    


 
   

# class AppointmentPhysio(models.Model):
#     STATUS_CHOICES = (
#         ('U', 'Upcoming'),
#         ('C', 'Completed'),
#     )
#     # slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     physiotherapist = models.ForeignKey(Physiotherapist, on_delete=models.CASCADE)
#     def __str__(self):
#         return f'Patient:{self.patient}, Physio:{self.physiotherapist}'   




