from django.shortcuts import render
from patient.models import Patient
from nurse.models import Nurse
from django.shortcuts import get_object_or_404, redirect
from .forms import Add_Profile, Modify_Profile, Booking_Form_Physio, Booking_Form_Nurse
from physiotherapist.models import Slot as PhysioSlot, Physiotherapist, BookingDate as PhysioDate, Slot as PhysioSlot
from nurse.models import Slot as NurseSlot, BookingDate as NurseDate, Slot as NurseSlot
from patient.forms import Appointment_Form_Physio, Appointment_Form_Nurse
from tests.models import Test
from django.http import JsonResponse
import random
import math
import json
from django.urls import reverse
from appointment.models import AppointmentNurse, AppointmentPhysio
from lab1.models import Lab1
from patient.models import LabBooking
from django.contrib.auth.models import User 


# Create your views here.


def home(request):
    user = request.user
    profile = Patient.objects.get(user=user)
    context = {
        'profile': profile
    }
    return render(request, 'patient/patient.html', context)


def modify_profile(request):
    user = request.user
    profile_item = Patient.objects.get(user=user)
    form = Modify_Profile(request.POST or None, instance=profile_item)
    if form.is_valid():
        form.save()
        return redirect('/patient/home/')
    return render(request, 'physiotherapist/new.html', {'form': form})


def book_physio(request):
    user = request.user
    form = Booking_Form_Physio(request.POST or None)
    if form.is_valid():
        return redirect('/patient/home/')
    profile = Patient.objects.get(user=user)
    first_name = profile.first_name
    last_name = profile.last_name
    context = {
        'physios': Physiotherapist.objects.all(),
        'first_name': first_name,
        'last_name': last_name,
    }
    print('context', context)
    return render(request, 'patient/make_booking.html', context)


def book_nurse(request):
    user = request.user
    form = Booking_Form_Nurse(request.POST or None)
    if form.is_valid():
        return redirect('/patient/home/')
    profile = Patient.objects.get(user=user)
    first_name = profile.first_name
    last_name = profile.last_name
    context = {
        'nurses': Nurse.objects.all(),
        'first_name': first_name,
        'last_name': last_name,
    }
    print('context', context)
    return render(request, 'patient/make_booking.html', context)


def buy_test(request):
    context = {
        'tests': Test.objects.all()
    }
    return render(request, 'patient/book_test.html', context=context)


def book_slot_physio(request, physio_id):
    user = request.user
    form = Appointment_Form_Physio(request.POST or None, physio_id=physio_id)
    if request.method == "POST":
        AppointmentPhysio.objects.create(
            patient_id=Patient.objects.get(user=user),
            physiotherapist_id=Physiotherapist.objects.get(pk=physio_id),
            slot_id=PhysioSlot.objects.get(pk=request.POST.get('slot_id')),
            OTP=12345,
            date=PhysioDate.objects.get(pk=request.POST.get('date')),
            status=False,
            problem=request.POST.get('problem'),
            description=request.POST.get('description')
        )
        slot = PhysioSlot.objects.get(pk=request.POST.get('slot_id'))
        slot.slot_status = True
        slot.save()
        # digits = [i for i in range(1, 10)]
        # random_str = ""
        # for i in range(6):
        #     index = math.floor(random.random() * 10)
        #     random_str += str(digits[index])
        # item.OTP = 123456
        # item.save()
        return redirect('/patient/book_physio/')
    context = {
        'form': form,
        'physio': True,
    }
    # print(form.is_valid(), form.errors)
    return render(request, 'patient/make_appointment_physio.html', context)


def book_slot_nurse(request, nurse_id):
    user = request.user
    form = Appointment_Form_Nurse(request.POST or None, nurse_id=nurse_id)
    if request.method == "POST":
        AppointmentNurse.objects.create(
            patient_id=Patient.objects.get(user=user),
            nurse_id=Nurse.objects.get(pk=nurse_id),
            slot_id=NurseSlot.objects.get(pk=request.POST.get('slot_id')),
            OTP=12345,
            date=NurseDate.objects.get(pk=request.POST.get('date')),
            status=False,
            problem=request.POST.get('problem'),
            description=request.POST.get('description')
        )
        slot = NurseSlot.objects.get(pk=request.POST.get('slot_id'))
        slot.slot_status = True
        slot.save()
        # digits = [i for i in range(1, 10)]
        # random_str = ""
        # for i in range(6):
        #     index = math.floor(random.random() * 10)
        #     random_str += str(digits[index])
        # item.OTP = 123456
        # item.save()
        return redirect('/patient/book_nurse/')
    context = {
        'form': form,
        'nurse': True,
    }
    return render(request, 'patient/make_appointment_nurse.html', context)

def load_slot_physio(request):
    date_id = request.GET.get('date')
    slots = PhysioSlot.objects.filter(date=date_id, slot_status=False)
    return render(request, 'patient/slot_option.html', {'slots': slots})

def load_slot_nurse(request):
    date_id = request.GET.get('date')
    slots = NurseSlot.objects.filter(date=date_id, slot_status=False)
    return render(request, 'patient/slot_option.html', {'slots': slots})

def filter_tests(request):
    keyword = request.GET.get('keyword')
    tests = Test.objects.filter(condition__startswith=keyword)
    return render(request, 'patient/filter_test.html', {'tests': tests})

def lab_lists(request, test_id):
    labs = Lab1.objects.all()
    return render(request, 'patient/lab-lists.html', {'labs': labs, 'test_id': test_id})

def book_test(request, test_id, lab_id):
    user = User.objects.get(pk = request.user.id)
    LabBooking.objects.create(patient = Patient.objects.get(user = user), lab = Lab1.objects.get(pk= lab_id), test = Test.objects.get(pk = test_id), status='Booked')
    return redirect(reverse('patient:bookings'))

def bookings(request):
    return render(request, 'patient/booking.html')

def appointments(request):
    return render(request, 'patient/appointment.html')