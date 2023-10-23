from django.urls import path, include
from forum.views import show_main

app_name = "book_page"

urlpatterns = [
    path('', show_main,name="show_main"), # ini buat nampilin api (json buku)
]
