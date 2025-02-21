from django.urls import path
from django.conf import settings
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [ 
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
]