from django.urls import path
from .views import *

urlpatterns = [
    path('physio/get/', api_get_physio.as_view()),
    path('nurse/get/', api_get_nurse.as_view()),
    path('patient/get/', api_get_patient.as_view()),
    path('report/get/', api_get_report.as_view()),
    path('test/get/', api_get_test.as_view()),
    path('test/get/<int:id>', api_get_test_one.as_view()),
    path('test/create', api_create_test.as_view()),
    ]