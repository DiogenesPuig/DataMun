from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.http import request

class UserForm(ModelForm):
    #last_name = forms.CharField(blank=False)
    #first_name = forms.CharField(blank=False)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    fields = ['basic_field']

class CenterForm(ModelForm):
    class Meta:
        model = Center
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CenterForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].required = True
        self.fields['longitude'].required = True
        self.fields['zone'].disabled = True
        self.fields['name'].disabled = True
        self.fields['code'].disabled = True
        
        
class CreateFileForm(ModelForm):
    #last_name = forms.CharField(blank=False)
    #first_name = forms.CharField(blank=False)
    class Meta:
        model = SpreadSheet
        fields = ['file']
        labels = {
            'watercourse': 'Spread Sheets: ',
        }

    def __init__(self, *args, **kwargs):
        super(CreateFileForm, self).__init__(*args, **kwargs)
        
        


class CreateUserForm(UserCreationForm):
    #last_name = forms.CharField(blank=False)
    #first_name = forms.CharField(blank=False)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

class DiagnosticForm(ModelForm):
    alert = forms.BooleanField()
    class Meta:
        model = Diagnostic
        fields = ['alert']
    def __init__(self, *args, **kwargs):
        super(DiagnosticForm, self).__init__(*args, **kwargs)
        self.fields['alert'].blank = False
