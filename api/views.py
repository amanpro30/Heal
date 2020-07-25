from django.shortcuts import render
from rest_framework import generics
from physiotherapist.models import Physiotherapist
from physiotherapist.models import Physiotherapist, Slot, BookingDate
from nurse.models import Nurse, Slot, BookingDate
from lab1.models import Lab1
from tests.models import Test
from patient.models import Patient, LabBooking
from samplecollector.models import SampleCollector
from report.models import Report, LabTest
from .serializers import PhysiotherapistSerializer, NurseSerializer, PatientSerializer, ReportSerializer, TestSerializer

# Create your views here.
class api_get_physio(generics.ListAPIView):
    queryset = Physiotherapist.objects.all()
    serializer_class = PhysiotherapistSerializer

class api_get_nurse(generics.ListAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

class api_get_patient(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class api_get_report(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class api_get_test(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class api_get_test_one(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Test.objects.filter(pk = id)

class api_create_test(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer