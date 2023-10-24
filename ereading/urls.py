from django.urls import path
from ereading.views import *

app_name = 'ereading'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard'),
    path('get-json/', get_json, name='get_json'),
    path('add-ereading/', add_ereading, name='add_ereading')
]
