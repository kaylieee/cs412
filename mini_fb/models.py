#Kaylie Leung kleung28@bu.edu
#Define app models
from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''
    Encapsulate the data of a Profile
    '''

    #define attributes
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''Return all of the status messages from this profile.'''

        status_messages = StatusMessage.objects.filter(profile=self).order_by('time_stamp')
        return status_messages
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk})

class StatusMessage(models.Model):
    '''
    Encapsulate the data of a Status Message
    '''

    #define attributes
    time_stamp = models.DateTimeField(blank=False)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.time_stamp}: {self.message}'