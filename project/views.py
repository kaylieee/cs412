#Kaylie Leung kleung28@bu.edu
#Define app views

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render

def placeholder_view(request):
    return HttpResponse("This view is under construction.")

class ShowAllInterestsView(ListView):
    '''
    Define a view class to show all course interests
    '''

    model = ClassInterest
    template_name = "project/all_interest_feed.html"
    context_object_name = "interests"

    def get_queryset(self):
        qs = super().get_queryset()

        if 'college' in self.request.GET:
            college = self.request.GET['college']
            if college:
                qs = qs.filter(section__course__college__iexact=college)
        if 'department' in self.request.GET:
            department = self.request.GET['department']
            if department:
                qs = qs.filter(section__course__department__iexact=department)
        if 'course_number' in self.request.GET:
            course_number = self.request.GET['course_number']
            if course_number:
                qs = qs.filter(section__course__course_number__iexact=course_number)
        if 'section_number' in self.request.GET:
            section_number = self.request.GET['section_number']
            if section_number:
                qs = qs.filter(section__section_number__iexact=section_number)
        return qs.order_by('-time')

class ShowStudentProfileView(DetailView):
    '''
    Define a view class to show a student profile
    '''

    model = Student
    template_name = "project/show_profile.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data(**kwargs)
        context['interests'] = ClassInterest.objects.filter(student=self.object)
        return context
    
class ShowMyProfileView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "project/show_profile.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data(**kwargs)
        context['interests'] = ClassInterest.objects.filter(student=self.object)
        return context

    def get_object(self):
        return Student.objects.get(user=self.request.user)

    def get_login_url(self):
        return reverse('login')

class DeleteRequestView(LoginRequiredMixin, DeleteView):
    '''A view to delete a request and remove it from the database.'''

    template_name = "project/delete_request_form.html"
    model = Request
    context_object_name = 'request'

    def get_success_url(self):
        return reverse('my_profile')
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
class CreateRequestView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Request.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Request object (POST)
    '''

    form_class = CreateRequestForm
    template_name = "project/create_request_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        context = super().get_context_data(**kwargs)

        student1 = Student.objects.get(pk=self.kwargs['other_pk'])
        student2 = Student.objects.get(user=self.request.user)
        student1Interests = ClassInterest.objects.filter(student=student1)
        student2Interests = ClassInterest.objects.filter(student=student2)
        context['student1'] = student1
        context['student2'] = student2
        context['student1Interests'] = student1Interests
        context['student2Interests'] = student2Interests
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        '''
        student1 = Student.objects.get(pk=self.kwargs['other_pk'])
        student2 = Student.objects.get(user=self.request.user)
        form.instance.student1 = student1
        form.instance.student2 = student2
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Request.'''

        student = Student.objects.get(user=self.request.user)
        return reverse('show_student', kwargs={'pk': student.pk})
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')

class UpdateStudentView(LoginRequiredMixin, UpdateView):
    '''A view to update a Student and save it to the database.'''
    
    model = Student
    form_class = UpdateStudentForm
    template_name = "project/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Student object.
        '''

        return super().form_valid(form)
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return Student.objects.get(user=self.request.user)
    
class CreateStudentView(CreateView):
    '''A view to handle creation of a new Student.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Student object (POST)
    '''

    form_class = CreateStudentForm
    template_name = "project/create_profile_form.html"

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
    
class ShowMyInterestsView(LoginRequiredMixin, ListView):
    '''
    Define a view class to show my course interests
    '''

    model = ClassInterest
    template_name = "project/my_interest_feed.html"
    context_object_name = "interests"

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.exclude(student__user=self.request.user)
        myWishlist = ClassInterest.objects.filter(interest_type="W", student__user=self.request.user).values_list("section", flat=True)
        myEnrolled = ClassInterest.objects.filter(interest_type="E", student__user=self.request.user).values_list("section", flat=True)

        hasMyWishlist = qs.filter(section__in=myWishlist, interest_type="E")
        hasMyEnrolled = qs.filter(section__in=myEnrolled, interest_type="E")

        qs = hasMyEnrolled|hasMyWishlist

        if 'college' in self.request.GET:
            college = self.request.GET['college']
            if college:
                qs = qs.filter(section__course__college__iexact=college)
        if 'department' in self.request.GET:
            department = self.request.GET['department']
            if department:
                qs = qs.filter(section__course__department__iexact=department)
        if 'course_number' in self.request.GET:
            course_number = self.request.GET['course_number']
            if course_number:
                qs = qs.filter(section__course__course_number__iexact=course_number)
        if 'section_number' in self.request.GET:
            section_number = self.request.GET['section_number']
            if section_number:
                qs = qs.filter(section__section_number__iexact=section_number)
        return qs.order_by('-time')
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
class CreateInterestView(LoginRequiredMixin, View):
    '''A view to handle creation of a new Student.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Student object (POST)
    '''

    template_name = "project/create_interest_form.html"
    
    def get(self, request, *args, **kwargs):
        context = {'type':  self.kwargs.get('type')}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        '''
        Handle the form submission to create a new Student object.
        '''

        college = request.POST.get('college')
        department = request.POST.get('department')
        course_number = request.POST.get('course_number')
        section_number = request.POST.get('section_number')

        #check if course exists if not, create
        if(Course.objects.filter(college=college, department=department, course_number=course_number).exists()):
            course = Course.objects.filter(college=college, department=department, course_number=course_number).first()
        else:
            course = Course(college=college, department=department, course_number=course_number)
            course.save()

        #check if section exists if not, create
        if(Section.objects.filter(course=course, section_number=section_number).exists()):
            section = Section.objects.filter(course=course, section_number=section_number).first()
        else:
            section = Section(course=course, section_number=section_number)
            section.save()
        
        course_interest = ClassInterest(student=Student.objects.filter(user=self.request.user).first(), interest_type=self.kwargs.get('type'), section=section)
        course_interest.save()


        return redirect('my_profile')

class DeleteInterestView(LoginRequiredMixin, DeleteView):
    '''A view to delete an interest and remove it from the database.'''

    template_name = "project/delete_request_form.html"
    model = ClassInterest
    context_object_name = 'interest'

    def get_success_url(self):
        return reverse('my_profile')
    
    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')