#Kaylie Leung kleung28@bu.edu
#Define app models
from django.db import models

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