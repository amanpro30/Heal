from django import forms
from .models import Report, Item
from dal import autocomplete
from .models import LabTest

class Make_Report(forms.ModelForm):
    class Meta:
        model=Report
        fields='__all__'

class ItemForm(forms.ModelForm):
    lab_test_name = forms.ModelChoiceField(
                queryset=LabTest.objects.all(),
                widget=autocomplete.ModelSelect2(url='report:name-autocomplete',
                attrs={
                'data-placeholder': 'Test-name',
                #'data-minimum-input-length': 1,
                })
            )
    class Meta:
        model = Item
        fields = ['lab_test_name','value',]
