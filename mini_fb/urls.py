#Kaylie Leung kleung28@bu.edu
#Define app URLs

from django.urls import path
from django.conf import settings
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView,CreateStatusMessageView,UpdateProfileView,DeleteStatusMessageView,UpdateStatusMessageView,AddFriendView,ShowFriendSuggestionsView,ShowNewsFeedView

urlpatterns = [ 
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status_message"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),
    
]