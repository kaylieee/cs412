#Kaylie Leung kleung28@bu.edu
#Define app views

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image, StatusMessage, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class ShowAllProfilesView(ListView):
    '''
    Define a view class to show all profiles
    '''

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''
    Define a view class to show all profiles
    '''

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):

        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user)
        form.instance.user = user

        return super().form_valid(form)

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Status Message.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Status Message object (POST)
    '''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_message_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data()
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Status Message
        object before saving it to the database.
        '''

		# instrument our code to display form fields: 
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        profile = Profile.objects.get(user=self.request.user)
        # attach this profile to the status message
        form.instance.profile = profile # set the FK

        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for f in files:
            image = Image(image_file = f, profile = profile)
            image.save()
            status_image = StatusImage(status_message = sm, image = image)
            status_image.save()

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Status Message.'''

        profile = Profile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update a Profile and save it to the database.'''
    
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''

        return super().form_valid(form)
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a status message and remove it from the database.'''

    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status_message'

    def get_success_url(self):
        # create and return a URL:
        # retrieve the PK from the URL pattern
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this status message is related by FK
        profile = status_message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view to update a status message and save it to the database.'''
    
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'status_message'
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Status Message object.
        '''

        return super().form_valid(form)

    def get_success_url(self):
        # create and return a URL:
        # retrieve the PK from the URL pattern
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this status message is related by FK
        profile = status_message.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

class AddFriendView(LoginRequiredMixin, View):
    '''
    Define a view class to add a friend
    '''

    def dispatch(self, request, *args, **kwargs):
        profile1 = Profile.objects.get(user=self.request.user)
        profile2 = Profile.objects.filter(pk=self.kwargs.get('other_pk')).first()
        profile1.add_friend(profile2)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''
    Define a view class to show all friend suggestions
    '''

    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''
    Define a view class to show news feed
    '''

    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
class ShowMyProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self):
        return reverse('login')