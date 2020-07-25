from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import SlotForm
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
from .forms import Add_Profile, Modify_Profile, Add_Test
from .models import Lab1, LabSlot1, Lab_complaint_feedback,BookingDateLab, Test1
from django.http import HttpResponseRedirect
from django.utils import timezone
from tests.models import Test
from patient.models import Patient, LabBooking
from samplecollector.models import SampleCollector



def lab_home(request):
    user = request.user 
    print(user)
    profile = Lab1.objects.get(user=user)  
    fb= Lab_complaint_feedback.objects.all()   
    context={
           'profile':profile
    }
    
    return render(request, 'lab1/profile_home.html',context)


def tests(request):
    user=request.user
    test = Test1.objects.all()
    profile=Lab1.objects.get(user=user)
    context = {
        "all_test": test,
        "profile":profile,
    }
    return render(request, 'lab1/test_list.html',context=context)
    
	 
	

# Create your views here.
# def home(request):
#     username = request.user.username
#     user_instance = User.objects.get(username=username)
#     physio_instance = Physiotherapist.objects.get(user=user_instance)
#     upcoming_appointments = AppointmentPhysio.objects.filter(physiotherapist=physio_instance, status='U')
#     completed_appointments = AppointmentPhysio.objects.filter(physiotherapist=physio_instance, status='C')
#     if request.method == 'GET':
#         slot_form = SlotForm()
#         # slot_form.fields['time_start'].widget = DateTimePickerInput()
#     elif request.method == 'POST':
#         slot_form = SlotForm(request.POST)
#         if slot_form.is_valid():
#             slot_form.save()    
#     return render(request, 'physiotherapist/physiotherapist1.html',{
#         'upcoming': upcoming_appointments,
#         'completed': completed_appointments,
#         'slot_form': slot_form,
#     })




def verification(request):
    return render(request,'lab1/verification.html')

def index(request):
    user=request.user
    profile=Lab1.objects.get(user=user)
    print(profile)
    context={
           'profile':profile
    }

    return render(request,'lab1/profile_home.html', context=context)


def make_profile(request):
    user = request.user
    if request.method=="POST":   
        form=Add_Profile(request.POST, request.FILES ,initial={'user':user,'email_id':user.email})

        if form.is_valid():
            profile_item=form.save(commit=False)
            profile_item.user = user
            profile_item.verified=False
            profile_item.email_id=user.email
            profile_item.save()

            # return render(request, "physiotherapist/verification.html", {})
            return redirect('/lab1/home/')


    else:

        form=Add_Profile(initial={'user':user,'email_id':user.email})
        #form.fields['user'].widget.attrs['disabled'] = True
        #form.fields['user'].editable=False
    return render(request,'lab1/make_profile.html',{'form':form})


def modify_profile(request):
    user = request.user
    profile_item = Lab1.objects.get(user=user)
    form=Modify_Profile(request.POST or None, instance=profile_item)
    if form.is_valid():
            form.save()
            return redirect('/lab1/home/')
    return render(request,'lab1/modify_profile.html',{'form':form})


def Show_Profile(request):
        user = request.user
        profile = Lab1.objects.get(user=user) 
        context={
            'profile':profile
        }
        if(profile.verified==True):
            # print('&&')
            return render(request,'lab1/show_profile.html',context)
        else:
            # print('%%')
            return redirect(reverse('lab1:verification'))

def create_slot(request, pk):
    user=request.user
    form = SlotForm(request.POST or None)
    date = get_object_or_404(BookingDateLab, pk=pk)
    if form.is_valid():

        item = form.save(commit=False)
        item.date = date
        profile = Lab1.objects.get(user=user)
        item.physiotherapist =profile
        try:
            item.save()
        except IntegrityError as e:
            context = {
                'date': date,
                'form': form,
                'message':"*Slot already Exists"
            }
            return render(request, 'lab1/create_slot.html', context)

        return redirect('/lab1/home/')
    context = {
        'date': date,
        'form': form,
    }

    return render(request, 'lab1/create_slot.html', context)

# @method_decorator(login_url=reverse_lazy('login'))
class DateCreate(CreateView):

    model=BookingDateLab
    fields=['date',]


    def get_initial(self):

         max_date=BookingDateLab.objects.all().aggregate(Max('date'))
        #  print(max_date)
        #  print(datetime)
         if max_date['date__max'] == None:
              max_date['date__max'] = timezone.now() + datetime.timedelta(days=1)
        #  print(max_date)     
         key, value = max_date.popitem()
        #  value += datetime.timedelta(days=1)
        #  print(value)
        # value=int(list(max_id.values())[0])
        # value=value+1
        # #user = request.user
        #
        #
        # #print(value)
         initial = super(DateCreate, self).get_initial()
         initial.update({'date': value})
         return initial
    def form_valid(self, form):
        user=self.request.user

        profile = Lab1.objects.get(user=user)
        date = form.save(commit=False)
        # print(date)
        try:
            obj = BookingDateLab.objects.filter(date=str(date)).filter(lab=profile).first()
        except BookingDate.DoesNotExist:
            obj = None
        # obj=get_object_or_404(BookingDate, date=str(date))
        # print('SHIVAM')
        # print(obj)
        #print(obj.pk)
        if(obj==None):
            # print("no")
            date.physiotherapist = profile
            return super(DateCreate, self).form_valid(form)
        else:
            # print('Yes')
            #return create_slot(self.request,pk=obj.pk-1)
            return redirect(str(obj.pk) + '/slot/')
            #return reverse('doctor_profile:create_slot',kwargs={'pk':int(obj.pk)})
            #return HttpResponse('OK')
            #return super(DateCreate, self).form_invalid(form)
        # context={
        #
		#     "object":appointment,
		# }
		# return render(self.request,'booking/booking_confirmation.html', context=context)


# @login_required(login_url=reverse_lazy('login'))
def show_slots(request):
    user=request.user
    profile = Lab1.objects.get(user=user)
    first_name=profile.first_name
    last_name=profile.last_name
    dates=Slot.objects.filter(physiotherapist=profile).order_by('start_time')
    print(dates)
    return render(request,'lab1/show_slots.html',{'slots':dates,'first_name':first_name,'last_name':last_name})

class ComplaintFeedbackCreate(CreateView):

    model= Lab_complaint_feedback
    fields=['specify_type','description']


    def form_valid(self, form):
        user=self.request.user

        profile = Lab1.objects.get(user=user)
        feedback = form.save(commit=False)
        feedback.physiotherapist = profile
        feedback.save()
        return redirect('/lab1/home/')
        # print(date)
        # try:
        #     obj = BookingDate.objects.filter(date=str(date)).filter(physiotherapist=profile).first()
        # except BookingDate.DoesNotExist:
        #     obj = None
        # # obj=get_object_or_404(BookingDate, date=str(date))
        # print('SHIVAM')
        # print(obj)
        # #print(obj.pk)
        # if(obj==None):
        #     print("no")
        #     date.physiotherapist = profile
        #     return super(DateCreate, self).form_valid(form)
        # else:
        #     print('Yes')
        #     #return create_slot(self.request,pk=obj.pk-1)
        #     return redirect(str(obj.pk) + '/slots/')
            #return reverse('doctor_profile:create_slot',kwargs={'pk':int(obj.pk)})
            #return HttpResponse('OK')
            #return super(DateCreate, self).form_invalid(form)
        # context={
        #
		#     "object":appointment,
		# }
		# return render(self.request,'booking/booking_confirmation.html', context=context)
def show_complaint_feedback(request):            
    user=request.user    
    profile = Lab1.objects.get(user=user)    
    lab_owner=profile.lab_owner    
    feedback=Lab_complaint_feedback.objects.filter(lab=profile)    
    # print(feedback)     
    return render(request,'lab1/show_profile.html',{'feedbacks':feedback,'lab_owner':lab_owner,})   

def delete_slot(request, slot_id):   
    # print(request.get['slot_id'])
    Slot.objects.filter(pk=slot_id).delete()
    return redirect('/lab1/slots/')

def collected_samples(request):
    user=request.user
    lab = Lab1.objects.get(user=user)
    bookings=LabBooking.objects.filter(lab_id=lab.id).filter(status='Collected')
    if not bookings:
        context= {
            "status":"Hurray No Pending Appointments",
            "profile":lab,
            "bookings":bookings,
           
        }
    else:
        context = {
        "status":"Upcoming Appointments",
        "bookings":bookings,
        "profile":lab,
        }
    return render(request,'lab1/collected_samples1.html',context=context)

def reports(request):
    user=request.user
    lab = Lab1.objects.get(user=user)
    bookings=LabBooking.objects.filter(lab_id=lab.id).filter(status='Completed')
    if not bookings:
        context= {
            "status":"No Appointments",
            "profile":lab,
            "bookings":bookings,
           
        }
    else:
        context = {
        "status":"Completed Appointments",
        "bookings":bookings,
        "profile":lab,
        }
    return render(request,'lab1/reports.html',context=context)


def show_bookings(request):
    user=request.user
    lab = Lab1.objects.get(user=user)
    bookings=LabBooking.objects.filter(lab_id=lab.id).filter(is_completed=False)
    if not bookings:
        context= {
            "status":"Hurray No Pending Appointments",
            "profile":lab,
            "bookings":bookings,
        }
    else:
        context = {
        "status":"Upcoming Appointments",
        "bookings":bookings,
        "profile":lab,
        }
    return render(request,'lab1/show_bookings.html',context=context)

def assign_collector(request):
    user=request.user
    lab = Lab1.objects.get(user=user)
    bookings=LabBooking.objects.filter(lab_id=lab.id).filter(status='Booked')
    if not bookings:
        context= {
            "status":"Hurray No Pending Appointments",
            "profile":lab,
            "bookings":bookings,
           
        }
    else:
        context = {
        "status":"Upcoming Appointments",
        "bookings":bookings,
        "profile":lab,
        }
    return render(request,'lab1/assign_collector.html',context=context)


def select_collector(request, pk):
    user=request.user
    booking = LabBooking.objects.get(pk=pk)
    samplecollectors=SampleCollector.objects.filter()
    context= {
            "status":"Hurray No Pending Appointments",
            "bookings":booking,
            "samplecollectors":samplecollectors,
        }
   
    return render(request,'lab1/select_collector.html',context=context)




def assign_collector_to_test(request, collector_id, booking_id):
    user=request.user
    bookings = LabBooking.objects.get(pk=booking_id)
    samplecollectors=SampleCollector.objects.get(pk=collector_id)
    bookings.collector=samplecollectors
    bookings.status="Sampled"
    bookings.save()
    context= {
            "status":"Hurray No Pending Appointments",
            "bookings":bookings,
            "samplecollectors":samplecollectors,
        }
   
    return redirect(reverse('lab1:lab_assign_collector'))




def add_test(request):
    user = request.user
    profile=Lab1.objects.get(user=user)
    if request.method=="POST":   
        form=Add_Test(request.POST, request.FILES ,initial={'user':user,})

        if form.is_valid():
            profile_item=form.save(commit=False)
            profile_item.user = user
            profile_item.save()

            # return render(request, "physiotherapist/verification.html", {})
            return redirect('/lab1/home/')


    else:

        form=Add_Test(initial={'user':user,})
        context = {
            "profile":profile,
            "form":form,
        }
    return render(request,'lab1/add_test.html',context=context)
