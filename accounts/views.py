from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



def index(request):
    context= { "a": "This is a context "}
    return render(request, 'account/rmp/login.html', context=context)