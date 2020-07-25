from django.shortcuts import render
from .models import Physiotherapist, Slot
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
from .forms import Add_Profile, Modify_Profile
from .models import BookingDate,Slot, Physiotherapist_complaint_feedback
from django.http import HttpResponseRedirect
from django.utils import timezone
from appointment.models import AppointmentPhysio


def physio_home(request):
    user = request.user
    profile = Physiotherapist.objects.get(user=user)
    fb= Physiotherapist_complaint_feedback.objects.all()
    # print(fb)
    context={
           'profile':profile
    }
    
    return render(request, 'physiotherapist/physiotherapist.html',context)

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
    return render(request,'physiotherapist/verification.html')

def index(request):
     #print(user)

    return render(request,'physiotherapist/profile_home.html')


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
            return redirect('/physiotherapist/home/')


    else:

        form=Add_Profile(initial={'user':user,'email_id':user.email})
        #form.fields['user'].widget.attrs['disabled'] = True
        #form.fields['user'].editable=False
    return render(request,'physiotherapist/new.html',{'form':form})


def modify_profile(request):
    user = request.user
    profile_item = Physiotherapist.objects.get(user=user)
    form=Modify_Profile(request.POST or None, instance=profile_item)
    if form.is_valid():
            form.save()
            return redirect('/physiotherapist/home/')
    return render(request,'physiotherapist/new.html',{'form':form})


def Show_Profile(request):
        user = request.user
        profile = Physiotherapist.objects.get(user=user)
        context={
            'profile':profile
        }
        if(profile.verified==True):
            # print('&&')
            return render(request,'physiotherapist/show_profile.html',context)
        else:
            # print('%%')
            return redirect(reverse('physiotherapist:verification'))

def create_slot(request, pk):
    user=request.user
    form = SlotForm(request.POST or None)
    date = get_object_or_404(BookingDate, pk=pk)
    if form.is_valid():

        item = form.save(commit=False)
        item.date = date
        profile = Physiotherapist.objects.get(user=user)
        item.physiotherapist =profile
        try:
            item.save()
        except IntegrityError as e:
            context = {
                'date': date,
                'form': form,
                'message':"*Slot already Exists"
            }
            return render(request, 'physiotherapist/create_slot.html', context)

        return redirect('/physiotherapist/home/')
    context = {
        'date': date,
        'form': form,
    }

    return render(request, 'physiotherapist/create_slot.html', context)

# @method_decorator(login_url=reverse_lazy('login'))
class DateCreate(CreateView):

    model=BookingDate
    fields=['date',]


    def get_initial(self):

         max_date=BookingDate.objects.all().aggregate(Max('date'))
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

        profile = Physiotherapist.objects.get(user=user)
        date = form.save(commit=False)
        # print(date)
        try:
            obj = BookingDate.objects.filter(date=str(date)).filter(physiotherapist=profile).first()
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
    profile = Physiotherapist.objects.get(user=user)
    first_name=profile.first_name
    last_name=profile.last_name
    dates=Slot.objects.filter(physiotherapist=profile).order_by('start_time')
    print(dates)
    return render(request,'physiotherapist/show_slots.html',{'slots':dates,'first_name':first_name,'last_name':last_name})

class ComplaintFeedbackCreate(CreateView):

    model= Physiotherapist_complaint_feedback
    fields=['specify_type','description']


    def form_valid(self, form):
        user=self.request.user

        profile = Physiotherapist.objects.get(user=user)
        feedback = form.save(commit=False)
        feedback.physiotherapist = profile
        feedback.save()
        return redirect('/physiotherapist/home/')
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
    profile = Physiotherapist.objects.get(user=user)
    first_name=profile.first_name
    last_name=profile.last_name
    feedback=Physiotherapist_complaint_feedback.objects.filter(physiotherapist=profile)
    # print(feedback)
    return render(request,'physiotherapist/show_feedback.html',{'feedbacks':feedback,'first_name':first_name,'last_name':last_name})

def delete_slot(request, slot_id):
    # print(request.get['slot_id'])
    Slot.objects.filter(pk=slot_id).delete()
    return redirect('/physiotherapist/slots/')


def show_appointments(request):
    user=request.user
    Physiotherapist = Physiotherapist.objects.get(user=user)
    appointments= PhysioAppoitments.objects.filter(physiotherapist_id=Physiotherapist).filter(is_attended=False).order_by('date').order_by('time')
    first_name=Physiotherapist.first_name
    last_name=Physiotherapist.last_name
    print(user)
    print(appointments)
    #print(prescriptions[0].pdf)
    #print(prescriptions[0].prescription_date)
    if not appointments:
        context="Hurray No Pending Appointments"
    else:
        context="Pending Appointments"
    # print(appointments[0].date)
    # print(appointments[0].time)
    return render(request,'phyiotherapist/physio_appointments.html',{'context':context,'appointments':appointments,'first_name':first_name,'last_name':last_name})

def attend_appointment(request, appointment_id):
    # print(request.get['slot_id'])
    appointment= PhysioAppoitments.objects.get(id=appointment_id)
    appointment.is_attended = True
    return redirect('/physiotherapist/home/')    

def show_appointments(request):
    user=request.user
    physiotherapist = Physiotherapist.objects.get(user=user)
    appointments= AppointmentPhysio.objects.filter(physiotherapist_id=physiotherapist).filter(status=False).order_by('date').order_by('slot_id')
    first_name=physiotherapist.first_name
    last_name=physiotherapist.last_name
    print(user)
    print(appointments)
    #print(prescriptions[0].pdf)
    #print(prescriptions[0].prescription_date)
    if not appointments:
        context="Hurray No Pending Appointments"
    else:
        context="Pending Appointments"
    # print(appointments[0].date)
    # print(appointments[0].time)
    return render(request,'physiotherapist/physio_appointments.html',{'context':context,'appointments':appointments,'first_name':first_name,'last_name':last_name})

def work_history(request):
    user=request.user
    physiotherapist = Physiotherapist.objects.get(user=user)
    appointments= AppointmentPhysio.objects.filter(physiotherapist_id=physiotherapist).filter(status=True).order_by('date').order_by('slot_id')
    first_name=physiotherapist.first_name
    last_name=physiotherapist.last_name
    print(user)
    print(appointments)
    #print(prescriptions[0].pdf)
    #print(prescriptions[0].prescription_date)
    if not appointments:
        context="Hurray No Pending Appointments"
    else:
        context="Pending Appointments"
    # print(appointments[0].date)
    # print(appointments[0].time)
    return render(request,'physiotherapist/work_history.html',{'context':context,'appointments':appointments,'first_name':first_name,'last_name':last_name})    

def attend_appointment(request, appointment_id):
    # print(request.get['slot_id'])
    appointment= AppointmentPhysio.objects.get(id=appointment_id)
    appointment.status = True
    appointment.save()
    return redirect('/physiotherapist/home/')      