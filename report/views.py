from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Report, LabTest
from .models import Item
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from .forms import Make_Report, ItemForm
from django.views import generic
from django.db.models import Max
from dal import autocomplete
from .utils import render_to_pdf
from django.template.loader import get_template
from io import BytesIO
from django.core.files import File
# from doctor_profile.models import Profile
from django.views.generic import FormView, CreateView
# from booking.models import AppointmentDetials
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from pprint import pprint
# Create your views here.
from django.contrib.auth.models import User
import time
from lab1.models import Lab1
from patient.models import LabBooking
from pprint import pprint

def index(request):
    return render(request,'report/report_home.html')

# @login_required(login_url=reverse_lazy('login'))
# def make_prescription(request):
#     if request.method=="POST":
#         form=Make_Report(request.POST)
#         if form.is_valid():
#             profile_item=form.save(commit=False)
#             profile_item.save()
#             #return redirect('/profile/show_profile/'+str(profile_item.doctor_id))
#     else:
#         form=Make_Prescription()
#     return render(request,'new_file.html',{'form':form})

class DetailView(generic.DetailView):
    model=Report
     
    template_name='report/detail.html'


class ReportCreate(CreateView):


    model=Report
    fields=['report_id',]
#################################TO PASS INITIAL VALUES ############
    def get_initial(self):
        booking_id=self.kwargs['booking_id']
        max_id=Report.objects.all().aggregate(Max('report_id'))
        if list(max_id.values())[0] == None:
            value=0
        else:
            value=int(list(max_id.values())[0])
        value=value+1
        #user = request.user


        #print(value)
        booking_id=self.kwargs['booking_id']
        initial = super(ReportCreate, self).get_initial()
        initial.update({'report_id': value})
        pprint('*')
        return initial

    def get_context_data(self, **kwargs):
        context = super(ReportCreate, self).get_context_data(**kwargs)
        user = self.request.user
        lab = Lab1.objects.get(user=user)
        booking = LabBooking.objects.get(id=self.kwargs['booking_id'])
        context['booking']= booking
        context['lab']= lab
        pprint(context)
        return context



    def form_valid(self, form):
        #event = Event.objects.get(pk=self.kwargs['appointment_id'])
        user=self.request.user
        lab = Lab1.objects.get(user=user)
        booking_id=int(self.kwargs['booking_id'])

        #print('**')
        report = form.save(commit=False)

        report.lab = Lab1.objects.get(user=user)
        report=form.save()
        booking = LabBooking.objects.get(id=self.kwargs['booking_id'])
        booking.status = 'Completed'
        booking.report = report
        booking.save()
        return super(ReportCreate, self).form_valid(form)

# @login_required(login_url=reverse_lazy('login'))
def detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'report/detail.html', {'report':report,'report_id':pk})

# @login_required(login_url=reverse_lazy('login'))
def create_item(request, report_id):
    form = ItemForm(request.POST or None, request.FILES or None , initial={'report':report_id})
    report = get_object_or_404(Report, pk=report_id)
    if form.is_valid():
        report_items = report.item_set.all()
        pprint(type(form.cleaned_data['lab_test_name']))
        for s in report_items:
            if s.lab_test_name == form.cleaned_data.get("lab_test_name").name :
                # print('**')
                context = {
                    'report': report,
                    'form': form,
                    'error_message': 'You already added that Test',
                }
                return render(request, 'report/create_item.html', context)
        item = form.save(commit=False)
        # print(item)
        lab_test = LabTest.objects.get(name=item.lab_test_name)
        item.lab_test = lab_test
        item.report = report
        item.save()
        return render(request, 'report/detail.html', {'report': report})
    context = {
        'report': report,
        'form': form,
    }
    return render(request, 'report/create_item.html', context)


class LabTestAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = LabTest.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        #print(qs)
        return qs


def print(request,report_id):
    report = get_object_or_404(Report, pk=report_id)
    report_no=int(report_id)
    report_no=report_no 

    template=get_template('report/print.html')
    context={"report_id":str(report_no),"report":report}
    html=template.render(context)
    pdf=render_to_pdf('report/print.html',context)
    filename ="report{}.pdf".format(report_id)

    if pdf:
        report.pdf.save(filename,File(BytesIO(pdf.content)))
        return HttpResponse(pdf,content_type='application/pdf')
       

    return HttpResponse('NOT FOUND')    
