from django.urls import path
from user_profile.views import *

app_name = 'user_profile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
    path('edit-profile',edit_profile, name='edit_profile'),
]