#Kaylie Leung kleung28@bu.edu
#Define app URLs

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('', ShowAllInterestsView.as_view(), name="show_all"),
    path('student/<int:pk>', ShowStudentProfileView.as_view(), name="show_student"),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
    path('profile/', ShowMyProfileView.as_view(), name="my_profile"),
    path('profile/<int:pk>/delete', DeleteRequestView.as_view(), name="delete_request"),
    path('swap/<int:other_pk>/', CreateRequestView.as_view(), name='create_request'),
    path('profile/update', UpdateStudentView.as_view(), name="update_student"),
    path('create_student', CreateStudentView.as_view(), name="create_student"),
    path('my_interests/', ShowMyInterestsView.as_view(), name="my_interests"),
    path('profile/create_interest/<str:type>/', CreateInterestView.as_view(), name="create_interest"),
    path('profile/delete_interest/<int:pk>/', DeleteInterestView.as_view(), name="delete_interest"),
]