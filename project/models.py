#Kaylie Leung kleung28@bu.edu
#Define app models
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    '''
    Encapsulate the data of a Student
    '''

    #define attributes
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_student', kwargs={'pk':self.pk})
    
    def get_pending_requests(self):
        '''Return request objects concerning student'''
        return Request.objects.filter(student1 = self)|Request.objects.filter(student2 = self)

class Course(models.Model):
    '''
    Encapsulate the data of a Course
    '''

    #define attributes
    college = models.TextField(blank=False)
    department = models.CharField(max_length=2)
    course_number = models.TextField(blank=False)

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.college}{self.department} {self.course_number}'

class Section(models.Model):
    '''
    Encapsulate the data of a Section
    '''

    #define attributes
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=2)

    def __str__(self):
         '''
         Return a string rep of this model instance
         '''
         return f'{self.course}: {self.section_number}'

class ClassInterest(models.Model):
    '''
    Encapsulate the data of a ClassInterest
    '''

    #define attributes
    INTEREST_CHOICES = {
        'E': 'Enrolled',
        'W': 'Wishlist',
    }

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    interest_type = models.CharField(max_length=1, choices=INTEREST_CHOICES)
    time = models.TimeField(auto_now=True)

class Request(models.Model):
    '''Encapsulate the data of a Request'''

    #define attributes
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student1') #recipient
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student2') #sender
    section1 = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section1')
    section2 = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section2')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student1} & {self.student2} swap {self.section1} & {self.section2}'