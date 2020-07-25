from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from lab1.models import Lab1





class Test(models.Model):
    CONDITION_CHOICES=(
        ('ALLERGY', 'ALLERGY'),
        ('ANEMIA', 'AMENIA'),
        
    )
    TEST_TYPE_CHOICES=(
        ('BLOOD', 'BLOOD'),
        ('URINE', 'URINE'),
    )
    profile_photo=models.ImageField(upload_to='media_/physio_profile_pic/')
    name=models.CharField(max_length =100, default='',)
    condition=models.CharField(max_length=100, default='', choices=CONDITION_CHOICES)
    test_type=models.CharField(max_length=100, default='', choices=TEST_TYPE_CHOICES)
    price=models.FloatField(default=0)
    discounted_price=models.FloatField(default=0)
    pre_test_information=models.CharField(max_length=256, default='')
    description=models.CharField(max_length=1000,default='')

    def __str__(self):
        return self.name


class TestLab(models.Model):
    lab = models.ForeignKey(Lab1, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)