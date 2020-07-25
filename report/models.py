from django.db import models
from django.urls import reverse
# from doctor_profile.models import Profile
from django.urls import reverse
from lab1.models import Lab1
# from patient.models import LabBooking

class Report(models.Model):
    lab=models.ForeignKey(Lab1,on_delete=models.CASCADE,null=True,blank=True)
    # booking=models.ForeignKey(LabBooking,on_delete=models.CASCADE,null=True,blank=True)
    report_id=models.CharField(max_length=30,unique=True)
    report_date=models.DateTimeField(auto_now_add=True)
    pdf= models.FileField(upload_to='media_/pdf/', null=True, blank=True)

    def __str__(self):
        return self.report_id

    def get_absolute_url(self):
        return reverse('report:detail',kwargs={'pk':self.pk})

class LabTest(models.Model):
    name=models.CharField(max_length=50)
    unit =models.CharField(max_length=10)
    min_value=models.CharField(max_length=100,blank=False)
    max_value=models.CharField(max_length=100,blank=False)

    def __str__(self):
        return self.name

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(name__lte=self.name)


class Item(models.Model):
    report=models.ForeignKey(Report,on_delete=models.CASCADE)
    lab_test_name=models.CharField(max_length=100,blank=False)
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    # days=models.BigIntegerField()
    value=models.CharField(max_length=100,blank=False) 
    # min_value=models.CharField(max_length=100,blank=False)
    # max_value=



    def __str__(self):
        return self.lab_test.name


