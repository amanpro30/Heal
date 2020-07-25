from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
from django.urls import reverse,reverse_lazy
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.utils import timezone
from tests.models import Test
from patient.models import Patient, LabBooking
from .models import *
from .forms import *
from lab1.models import Lab1



def sample_collector_home(request):
    user = request.user 
    print(user)
    profile = SampleCollector.objects.get(user=user)  
    context={
           'profile':profile
    }
    
    return render(request, 'samplecollector/profile_home.html',context)


def make_profile(request):
    user = request.user
    if request.method=="POST":   
        form=Add_Profile(request.POST, request.FILES ,initial={'user':user,})

        if form.is_valid():
            profile_item=form.save(commit=False)
            profile_item.user = user
            profile_item.save()

            # return render(request, "physiotherapist/verification.html", {})
            return redirect('/samplecommector/')


    else:

        form=Add_Profile(initial={'user':user,})
        #form.fields['user'].widget.attrs['disabled'] = True
        #form.fields['user'].editable=False
    return render(request,'samplecollector/make_profile.html',{'form':form})


def modify_profile(request):
    user = request.user
    profile_item = SampleCollector.objects.get(user=user)
    form=Modify_Profile(request.POST or None, instance=profile_item)
    if form.is_valid():
            form.save()
            return redirect(reverse('samplecollector:collector_home'))
    return render(request,'samplecollector/modify_profile.html',{'form':form})



def samples_to_be_collected(request):
    user=request.user
    samplecollector = SampleCollector.objects.get(user=user)
    bookings=LabBooking.objects.filter(collector_id=samplecollector.id).filter(status='Sampled')
    if not bookings:
        context= {
            "status":"Hurray No Pending Work",
            "profile":samplecollector,
            "bookings":bookings,
           
        }
    else:
        context = {
        "status":"Upcoming Pickups",
        "bookings":bookings,
        "profile":samplecollector,
        }
    return render(request,"samplecollector/assigned_samples.html",context=context)

def collected_samples(request):
    user=request.user
    samplecollector = SampleCollector.objects.get(user=user)
    bookings=LabBooking.objects.filter(collector_id=samplecollector.id).filter(status='Collected')
    if not bookings:
        context= {
            "status":"Samples Not Collected Yet",
            "profile":samplecollector,
            "bookings":bookings,
           
        }
    else:
        context = {
        "status":"Upcoming Pickups",
        "bookings":bookings,
        "profile":samplecollector,
        }
    return render(request,"samplecollector/collected_samples.html",context=context)



def collection_details(request, booking_id):
    user=request.user
    booking = LabBooking.objects.get(pk=booking_id)
    patient_id=booking.patient.id
    lab_id=booking.lab.id
    patient_object=Patient.objects.get(pk=patient_id)
    lab_object=Lab1.objects.get(pk=patient_id)
    print(patient_id)
    context= {
            "booking":booking,
            "patient_object":patient_object,
            "lab_object":lab_object,

        }
   
    return render(request,'samplecollector/collection_details.html',context=context)




def confirm_collection(request, booking_id):
    user=request.user
    bookings = LabBooking.objects.get(pk=booking_id)
    bookings.status="Collected"
    bookings.save()
    context= {
            "status":"Hurray No Pending Appointments",
            "bookings":bookings,
        }
   
    return redirect(reverse('samplecollector:collector_assigned_samples'))

def collector_collected_details(request, booking_id):
    user=request.user
    booking = LabBooking.objects.get(pk=booking_id)
    patient_id=booking.patient.id
    lab_id=booking.lab.id
    patient_object=Patient.objects.get(pk=patient_id)
    lab_object=Lab1.objects.get(pk=patient_id)
    print(patient_id)
    context= {
            "booking":booking,
            "patient_object":patient_object,
            "lab_object":lab_object,

        }
   
    return render(request,'samplecollector/collector_collected_details.html',context=context)


# def add_test(request):collector_collected_details
#     user = request.user
#     profile=Lab1.objects.get(user=user)
#     if request.method=="POST":   
#         form=Add_Test(request.POST, request.FILES ,initial={'user':user,})

#         if form.is_valid():
#             profile_item=form.save(commit=False)
#             profile_item.user = user
#             profile_item.save()

#             # return render(request, "physiotherapist/verification.html", {})
#             return redirect('/lab1/home/')


#     else:

#         form=Add_Test(initial={'user':user,})
#         context = {
#             "profile":profile,
#             "form":form,
#         }
#     return render(request,'lab1/add_test.html',context=context)
