from django.urls import path, include
from user_profile.views import profile, create_profile, cari_buku, rekomen, delete_account, get_json, create_profile_flutter, edit_profile_flutter, get_allaccount_json, delete_account_flutter

app_name = "user_profile"
urlpatterns = [
    path('', profile, name='profile'),
    path('create_profile/', create_profile, name='create_profile'),
    path('cari-buku/', cari_buku, name='cari_buku'),
    path('rekomen/', rekomen, name='rekomen'),
    path('delete_account/<int:id>/', delete_account, name='delete_account'),
    path('json/', get_json, name='get_json'),
    path('get-allaccount/', get_allaccount_json, name='get_allaccount_json'),
    path('create-profile-flutter/', create_profile_flutter, name='create_profile_flutter'),
    path('edit-profile-flutter/<int:id>/', edit_profile_flutter, name='edit_profile_flutter'),
    path('delete-account-flutter/<int:id>/', delete_account_flutter, name="delete_account_flutter"),
]
