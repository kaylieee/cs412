from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(ClassInterest)
admin.site.register(Request)