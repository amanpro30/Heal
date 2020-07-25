from physiotherapist.models import Physiotherapist, Slot, BookingDate
from nurse.models import Nurse, Slot, BookingDate
from lab1.models import Lab1
from tests.models import Test
from patient.models import Patient, LabBooking
from samplecollector.models import SampleCollector
from report.models import Report, LabTest, Item
from rest_framework import serializers
from datetime import timezone, datetime


class PhysiotherapistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physiotherapist
        fields = ['first_name', 'last_name', 'age', 'speciality', 'experience',
                  'house_no', 'city', 'state', 'pin', 'gender', 'dob', 'mob_no']


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['first_name', 'last_name', 'age', 'experience',
                  'house_no', 'city', 'state', 'pin', 'gender', 'dob', 'mob_no']


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab1
        fields = ['lab_name',
                  'lab_registration',
                  'lab_owner',
                  'lab_address',
                  'mobile_no',
                  'house_no',
                  'city',
                  'state',
                  'pin',
                  'rating',
                  'verified'
                  ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'age',
                  'house_no', 'city', 'state', 'pin', 'gender', 'dob', 'mob_no']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['report_date', 'pdf']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name',
                  'condition',
                  'test_type',
                  'price',
                  'discounted_price',
                  'pre_test_information',
                  'description']
