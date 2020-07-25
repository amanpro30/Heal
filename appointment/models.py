from django.db import models
from patient.models import Patient
from physiotherapist.models import Physiotherapist, Slot as PhysioSlot, BookingDate as PhysioBookingDate
from nurse.models import Nurse, Slot as NurseSlot, BookingDate as NurseBookingDate

# Create your models here.

class AppointmentPhysio(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    physiotherapist_id = models.ForeignKey(
        Physiotherapist, on_delete=models.CASCADE)
    slot_id = models.ForeignKey(PhysioSlot, on_delete=models.CASCADE)
    OTP = models.IntegerField()
    date = models.ForeignKey(PhysioBookingDate, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    problem = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=250, null=True)

class AppointmentNurse(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse_id = models.ForeignKey(
        Nurse, on_delete=models.CASCADE)
    slot_id = models.ForeignKey(NurseSlot, on_delete=models.CASCADE)
    OTP = models.IntegerField()
    date = models.ForeignKey(NurseBookingDate, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    problem = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=250, null=True)