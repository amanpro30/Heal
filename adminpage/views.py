from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse,reverse_lazy
from .forms import Add_Test
from patient.models import Patient
from physiotherapist.models import Physiotherapist
from nurse.models import Nurse
from lab1.models import Lab1
from samplecollector.models import SampleCollector

def adminpage(request):
    print(request.user)
    user_instance = User.objects.get(username=request.user.username)
    if(Patient.objects.filter(user=user_instance)):
        return redirect('/patient/home')
    if(Physiotherapist.objects.filter(user=user_instance)):
        return redirect('/physiotherapist/home')
    if(Nurse.objects.filter(user=user_instance)):
        return redirect('/nurse/home')
    if(Lab1.objects.filter(user=user_instance)):
        return redirect('/lab1')
    if(SampleCollector.objects.filter(user=user_instance)):
        return redirect('/samplecollector')

def add_new_test(request):
    if request.method=="POST":
        form=Add_Test(request.POST, request.FILES)

        if form.is_valid():
            test_item=form.save(commit=False)
            test_item.test_id='TEST001'
            test_item.save()

            return redirect('adminpage:adminpage')


    else:

        form=Add_Test()
        #form.fields['user'].widget.attrs['disabled'] = True
        #form.fields['user'].editable=False
    return render(request, 'adminpage/new_test.html', {'form':form})   