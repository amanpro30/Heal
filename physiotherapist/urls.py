from django.conf.urls import url
from django.urls import path
from . import views
from .views import *



app_name='physiotherapist'

urlpatterns = [
    path('',views.index,name='index'),
    # path('slot/', views.home),
    path('make_profile/',views.make_profile,name='make_profile'),
    path('modify_profile/',views.modify_profile,name='modify_profile'),
    path('show_profile/',views.Show_Profile,name='show_profile'),
    path('home/', physio_home, name='home'),
    path('date_add/',views.DateCreate.as_view(),name='Date_Create'),
    url(r'^date_add/(?P<pk>[0-9]+)/slot/$', views.create_slot, name='create_slot'),
    path('slots/',views.show_slots,name='show_slots'),
    path('complaint_feedback/', views.ComplaintFeedbackCreate.as_view(), name='complaint_feedback'),
    path('show_complaint_feedback/', views.show_complaint_feedback, name='show_complaint_feedback'),
    url(r'^delete_slot/(?P<slot_id>[0-9]+)$',views.delete_slot,name='delete_slot'),
    
    path('appointments/',views.show_appointments,name='show_appointments'),
    path('work_history/',views.work_history,name='work_history'),
    # path('attend_appointment',views.show_slots,name='show_slots'),
    url(r'^attend_appointment/(?P<appointment_id>[0-9]+)$',views.attend_appointment,name='attend_appointment'),
    ]
