from django.db import models
from django.contrib.auth.models import User

from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from django.urls import reverse
from samplecollector.models import *

# Create your models here.
class Lab1(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length =100, default='')
    lab_registration = models.CharField(max_length =100, default='')
    lab_owner = models.CharField(max_length=350)
    lab_address = models.CharField(max_length =300, default='')
    mobile_no=models.BigIntegerField()
    profile_photo=models.ImageField(upload_to='media_/physio_profile_pic/')
    house_no = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin = models.IntegerField()
    rating = models.FloatField(default=0.0)
    verified = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('lab1:verification', kwargs={'pk':self.pk})
    
    
    def __str__(self):
        return f'{self.lab_owner}'

class LabSlot1(models.Model):
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    def __str__(self):
        return f'{self.time_start} to {self.time_end}'

class BookingDateLab(models.Model):
    lab=models.ForeignKey(Lab1,on_delete=models.CASCADE, null=True,blank=True)
    date=models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.date)
    def get_absolute_url(self):
        return reverse('lab1:create_slot',kwargs={'pk':self.pk})

class SampleCollectionSlot(models.Model):
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
    lab=models.ForeignKey(Lab1,on_delete=models.CASCADE, null=True,blank=True)
    date=models.ForeignKey(BookingDateLab,on_delete=models.CASCADE, null=True,blank=True)
    start_time=models.CharField(max_length=200,choices=TIME_CHOICES,null=True,blank=True)
    slot_status=models.BooleanField(default=False)

    class Meta:
        unique_together = ('lab','start_time','date')

    def __str__(self):
    	return str(self.start_time)

class Lab_complaint_feedback(models.Model):
    COMPLAINT_CHOICES = (
        ('SALARY', 'SALARY'),
        ('BOOKING', 'BOOKING'),
        ('OTHER/FEEDBACK','OTHER/FEEDBACK')
    )
    STATUS_CHOICES = (
        ('SENT TO ADMIN', 'SENT TO ADMIN'),
        ('RESOLVED', 'RESOLVED'),
    )

    lab=models.ForeignKey(Lab1,on_delete=models.CASCADE, null=True,blank=True)
    specify_type=models.CharField(max_length=200,choices=COMPLAINT_CHOICES,null=False,blank=False)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=200,choices=STATUS_CHOICES,default='SENT TO ADMIN')
    description=models.TextField(null=False, blank=False)


class Test1(models.Model):
    CONDITION_CHOICES=(
        ('ALLERGY', 'ALLERGY'),
        ('ANEMIA', 'AMENIA'),
        
    )
    TEST_TYPE_CHOICES=(
        ('BLOOD', 'BLOOD'),
        ('URINE', 'URINE'),
    )
    
    name=models.CharField(max_length =100, default='',)
    condition=models.CharField(max_length=100, default='', choices=CONDITION_CHOICES)
    test_type=models.CharField(max_length=100, default='', choices=TEST_TYPE_CHOICES)
    price=models.FloatField()
    discounted_price=models.FloatField()
    pre_test_information=models.CharField(max_length=256, default='')
    description=models.CharField(max_length=1000,default='')
    photo=models.ImageField(upload_to='media_/lab_pics/', null=True)
    collector=models.ForeignKey(SampleCollector, on_delete=models.CASCADE, null=True,blank=True)


    
    def get_absolute_url(self):
        return reverse('lab1:assign_collector_to_test', kwargs={'pk':self.pk})
    
    

    def __str__(self):
        return self.name


