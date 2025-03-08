#Kaylie Leung kleung28@bu.edu
#Define app views

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Image, StatusMessage, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse

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

class CreateStatusMessageView(CreateView):
    '''A view to handle creation of a new Status Message.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Status Message object (POST)
    '''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_message_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
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
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
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

        # create and return a URL:
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk':pk})

class UpdateProfileView(UpdateView):
    '''A view to update a Profile and save it to the database.'''
    
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''

        return super().form_valid(form)

class DeleteStatusMessageView(DeleteView):
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

class UpdateStatusMessageView(UpdateView):
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
