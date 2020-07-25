from django.conf.urls import url
from django.urls import path
from . import views

app_name='report'

urlpatterns=[
    path('',views.index,name='index'),
    # url(r'^prescription_add/(?P<appointment_id>[0-9]+)$',views.PrescriptionCreate.as_view(),name='Prescription_Add1'),
    url(r'^report_add/(?P<booking_id>[0-9]+)$',views.ReportCreate.as_view(),name='Report_Add1'),
    # path('prescription_add/',views.make_prescription,name='Prescription_Add'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<report_id>[0-9]+)/create_item/$', views.create_item, name='create_item'),
    path('name-autocomplete/',views.LabTestAutocomplete.as_view(),name='name-autocomplete'),
    url(r'^(?P<report_id>[0-9]+)/print/$', views.print, name='print'),

]