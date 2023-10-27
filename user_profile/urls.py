from django.urls import path
from user_profile.views import *

app_name = 'user_profile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
    path('get-profile/', get_profile_json, name='get_profile_json'),    
    path('create-profile',create_profile, name='create_profile'),
    path('edit-profile',edit_profile, name='edit_profile'),
]