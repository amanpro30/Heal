from django.conf.urls import url
from django.urls import path
from . import views
from .views import *



app_name='samplecollector'

urlpatterns = [
    path('',views.sample_collector_home,name='collector_home'),
    path('make_profile/',views.make_profile,name='collector_make_profile'),
    path('modify_profile/',views.modify_profile,name='collector_modify_profile'),
    path('assigned_samples/',views.samples_to_be_collected, name='collector_assigned_samples'),
    path('collected_samples/',views.collected_samples, name='collector_collected_samples'),
    url(r'^confirm_collection/(?P<booking_id>\w+)/$',views.confirm_collection,name='confirm_collection'),
    url(r'^collection_details/(?P<booking_id>\w+)/$',views.collection_details,name='collector_collection_details'),
    url(r'^collector_collected_details/(?P<booking_id>\w+)/$',views.collector_collected_details,name='collector_collected_details'),
    
    
    ]
