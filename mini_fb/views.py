#Kaylie Leung kleung28@bu.edu
#Define app views

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm, CreateStatusMessageForm
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

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Status Message.'''

        # create and return a URL:
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk':pk})