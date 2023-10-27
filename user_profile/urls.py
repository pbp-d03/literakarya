from django.urls import path
from user_profile.views import profile, create_profile

urlpatterns = [
    path('', profile, name='profile'),
    path('create_profile/', create_profile, name='create_profile'),
]
