#Kaylie Leung kleung28@bu.edu
#Define app URLs

from django.urls import path
from django.conf import settings
from .views import ShowAllVotersView, ShowVoterView
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('', ShowAllVotersView.as_view(), name="voters"),
    path('voter/<int:pk>', ShowVoterView.as_view(), name="voter"),
]