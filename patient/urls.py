from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('modify_profile/', views.modify_profile, name='modify_profile'),
    path('book_physio/', views.book_physio, name='book_physio'),
    path('book_nurse/', views.book_nurse, name='book_nurse'),
    url(r'^book_slot_physio/(?P<physio_id>[0-9]+)$',
        views.book_slot_physio, name='book_slot_physio'),
    url(r'^book_slot_nurse/(?P<nurse_id>[0-9]+)$',
        views.book_slot_nurse, name='book_slot_nurse'),
    path('buy_test/', views.buy_test, name='buy_test'),
    path('ajax/load-slots-physio/', views.load_slot_physio,
         name='ajax_load_slots_physio'),
    path('ajax/load-slots-nurse/', views.load_slot_nurse,
         name='ajax_load_slots_nurse'),
    path('ajax/filter-tests/', views.filter_tests, name='filter_tests'),
    url(r'^lab_lists/(?P<test_id>[0-9]+)$',
        views.lab_lists, name='lab_lists'),
    url(r'^book_test/(?P<test_id>\w+)/(?P<lab_id>\w+)/$',
        views.book_test, name='book_test'),
    path('lab-test/', views.bookings, name='lab-test'),
    path('appointment/', views.appointments, name='appointment')
]
