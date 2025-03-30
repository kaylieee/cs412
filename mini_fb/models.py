#Kaylie Leung kleung28@bu.edu
#Define app models
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    
    def get_friends(self):
        '''Return all of the friends from this profile.'''

        friends = set()
        friendships = Friend.objects.filter(friend1 = self) | Friend.objects.filter(friend2 = self)
        for friendship in friendships:
            if friendship.friend1 == self:
                friends.add(friendship.friend2)
            else:
                friends.add(friendship.friend1)
        return list(friends)
    
    def add_friend(self, other):
        '''Add a friend to this profile.'''
        if self == other:
            print('ERROR: Can not add self as friend')
        else:
            if Friend.objects.filter(friend1 = self, friend2 = other).first() == None and Friend.objects.filter(friend1 = other, friend2 = self).first() == None:
                newFriend = Friend(friend1=self, friend2=other)
                newFriend.save()
            else:
                print('ERROR: Tried add duplicate friend')
    
    def get_friend_suggestions(self):
        '''Get friend suggestions for this profile.'''
        current_friends = self.get_friends()

        current_friend_ids = [friend.pk for friend in current_friends]
        current_friend_ids.append(self.pk)

        return Profile.objects.exclude(pk__in=current_friend_ids)
    
    def get_news_feed(self):
        '''Get news feed for this profile.'''
        current_friends = self.get_friends()
        current_friends.append(self)

        return StatusMessage.objects.filter(profile__in=current_friends).order_by('time_stamp')

class StatusMessage(models.Model):
    '''
    Encapsulate the data of a Status Message
    '''

    #define attributes
    time_stamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.time_stamp}: {self.message}'
    
    def get_images(self):
        '''Return all of the images from this status message.'''

        status_images = StatusImage.objects.filter(status_message=self)
        images = [status_image.image for status_image in status_images]
        return images

class Image(models.Model):
    '''Encapsulate the data of an Image'''

    #define attributes
    image_file = models.ImageField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(null=True, blank=True)

class StatusImage(models.Model):
    '''Encapsulate the data of a Status Image'''

    #define attributes
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

class Friend(models.Model):
    '''Encapsulate the data of a Friend'''

    #define attributes
    friend1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    friend2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.friend1} & {self.friend2}'
