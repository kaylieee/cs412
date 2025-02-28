#Kaylie Leung kleung28@bu.edu
#Define app forms

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Status Message to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = StatusMessage
        fields = ['time_stamp', 'message']