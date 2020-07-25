from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from django.urls import reverse

# Create your models here.
class Physiotherapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Undisclosed'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    speciality = models.CharField(max_length=20)
    experience = models.IntegerField(default=0, null=True)
    profile_photo=models.ImageField(upload_to='media_/physio_profile_pic/')
    house_no = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin = models.IntegerField()
    gender = models.CharField(max_length=1, choices=gender_choices)
    dob = models.DateField()
    mob_no = models.BigIntegerField()
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return f'{self.first_name}'

class Slot1(models.Model):
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    def __str__(self):
        return f'{self.time_start} to {self.time_end}'

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

class BookingDate(models.Model):
    physiotherapist=models.ForeignKey(Physiotherapist,on_delete=models.CASCADE, null=True,blank=True)
    date=models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.date)
    def get_absolute_url(self):
        return reverse('physiotherapist:create_slot',kwargs={'pk':self.pk})

class Slot(models.Model):
    TIME_CHOICES = (('09:00:00', '9 am'),
                    ('10:00:00', '10 am'),
                    ('11:00:00', '11 am'),
                    ('12:00:00', '12 pm'),
                    ('13:00:00', '1 pm'),
                    ('14:00:00', '2 pm'),
                    ('15:00:00', '3 pm'),
                    ('16:00:00', '4 pm'),
                    ('17:00:00', '5 pm'),
                    ('18:00:00', '6 pm'), )
    physiotherapist=models.ForeignKey(Physiotherapist,on_delete=models.CASCADE, null=True,blank=True)
    date=models.ForeignKey(BookingDate,on_delete=models.CASCADE, null=True,blank=True)
    start_time=models.CharField(max_length=200,choices=TIME_CHOICES,null=True,blank=True)
    slot_status=models.BooleanField(default=False)

    class Meta:
        unique_together = ('physiotherapist','start_time','date')

    def __str__(self):
    	return str(self.start_time)

class Physiotherapist_complaint_feedback(models.Model):
    COMPLAINT_CHOICES = (
        ('SALARY', 'SALARY'),
        ('BOOKING', 'BOOKING'),
        ('OTHER/FEEDBACK','OTHER/FEEDBACK')
    )
    STATUS_CHOICES = (
        ('SENT TO ADMIN', 'SENT TO ADMIN'),
        ('RESOLVED', 'RESOLVED'),
    )

    physiotherapist=models.ForeignKey(Physiotherapist,on_delete=models.CASCADE, null=True,blank=True)
    specify_type=models.CharField(max_length=200,choices=COMPLAINT_CHOICES,null=False,blank=False)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200,choices=STATUS_CHOICES,default='SENT TO ADMIN')
    description=models.TextField(null=False, blank=False)