from django import forms
from tests.models import Test

class Add_Test(forms.ModelForm):

   
    class Meta:
        model=Test
        exclude = ('test_id',)

    