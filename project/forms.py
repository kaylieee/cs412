#Kaylie Leung kleung28@bu.edu
#Define app forms

from django import forms
from .models import *
from django.forms import TextInput

class CreateRequestForm(forms.ModelForm):
    '''A form to add a Request to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Request
        fields = ['section1', 'section2']

class UpdateStudentForm(forms.ModelForm):
    '''A form to update a Student in the database.'''

    class Meta:
        '''associate this form with the Student model.'''
        model = Student
        fields = ['email_address']
        widgets = {
            "email_address": TextInput(),
        }

class CreateStudentForm(forms.ModelForm):
    '''A form to add a Student to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Student
        fields = ['first_name', 'last_name', 'email_address']
        widgets = {
            "first_name": TextInput(),
            "last_name": TextInput(),
            "email_address": TextInput(),
        }

class CreateInterestForm(forms.Form):
    '''A form to add an Interest to the database.'''
    college = forms.CharField()
    department = forms.CharField()
    course_number = forms.CharField()
    section_number = forms.CharField()