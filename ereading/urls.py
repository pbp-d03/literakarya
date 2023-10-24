from django.urls import path
from ereading.views import *

app_name = 'ereading'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard')
]
