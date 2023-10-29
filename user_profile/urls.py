from django.urls import path, include
from user_profile.views import profile, create_profile, cari_buku, rekomen

app_name = "user_profile"
urlpatterns = [
    path('', profile, name='profile'),
    path('create_profile/', create_profile, name='create_profile'),
    path('cari-buku/', cari_buku, name='cari_buku'),
    path('rekomen/', rekomen, name='rekomen'),
]
