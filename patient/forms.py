from django.forms import ModelForm
from django import forms
from .models import Patient
from physiotherapist.models import Slot as PhysioSlot, BookingDate as PhysioDates,  Physiotherapist
from nurse.models import Slot as NurseSlot, Nurse, BookingDate as NurseDates
from appointment.models import AppointmentNurse, AppointmentPhysio


class Modify_Profile(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('user', 'gender', 'verified', 'rating')

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data['mobile_no']
        if len(str(mobile_no)) != 10:
            raise forms.ValidationError('enter  a 10 digit number')
        return self.cleaned_data['mobile_no']


class Add_Profile(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(
        attrs={
        'type': 'date',
        }
        )
    )

    class Meta:
        model = Patient
        exclude = ('user', 'verified', 'email_id',)

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data['mobile_no']
        if len(str(mobile_no)) != 10:
            raise forms.ValidationError('enter  a 10 digit number')
        return self.cleaned_data['mobile_no']


class Booking_Form_Physio(forms.ModelForm):
    class Meta:
        model = PhysioSlot
        exclude = ('slot_status',)


class Booking_Form_Nurse(forms.ModelForm):
    class Meta:
        model = NurseSlot
        exclude = ('slot_status',)


class Appointment_Form_Physio(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control col-md-6',
        }
    ))
    problem = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control col-md-6',
        }
    ))

    class Meta:
        model = AppointmentPhysio
        exclude = ('OTP', 'status', 'patient_id', 'physiotherapist_id')

    def __init__(self, *args, **kwargs):
        self.physio_id = kwargs.pop('physio_id')
        super(Appointment_Form_Physio, self).__init__(*args, **kwargs)
        self.fields['slot_id'].queryset = PhysioSlot.objects.none()
        self.physiotherapist = Physiotherapist.objects.get(pk = self.physio_id)
        self.fields['date'].queryset = PhysioDates.objects.filter(physiotherapist=self.physiotherapist)
        

class Appointment_Form_Nurse(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control col-md-6',
        }
    ))
    problem = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control col-md-6',
        }
    ))
    slot_id = forms.CheckboxSelectMultiple()

    class Meta:
        model = AppointmentNurse
        exclude = ('OTP', 'status', 'patient_id', 'nurse_id')

    def __init__(self, *args, **kwargs):
        self.nurse_id = kwargs.pop('nurse_id')
        super(Appointment_Form_Nurse, self).__init__(*args, **kwargs)
        self.fields['slot_id'].queryset = NurseSlot.objects.none()
        self.nurse = Nurse.objects.get(pk = self.nurse_id)
        self.fields['date'].queryset = NurseDates.objects.filter(nurse=self.nurse)
