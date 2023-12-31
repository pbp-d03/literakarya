from django.urls import path
from ereading.views import *

app_name = 'ereading'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard'),
    path('get-json/', get_json, name='get_json'),
    path("get-json/<str:uname>/",get_json_user, name="get_json_user"),
    path('add-ereading/', add_ereading, name='add_ereading'),
    path('add-ereading-flutter/', add_ereading_flutter, name='add_ereading_flutter'),
    path('delete-ereading/', delete_ereading, name='delete_ereading'),
    path('accept-ereading/', accept_ereading, name='accept_ereading'),
    path('reject-ereading/', reject_ereading, name='reject_ereading'),
]