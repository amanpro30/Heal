from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect



def home_page(request):
	return render(request, "home.html")



def log_out(request):
	logout(request)

	return redirect('/')
